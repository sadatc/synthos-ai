from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO

from .agents_builtin import EchoAgent, ShellAgent, WebGetAgent
from .agents_cursor import CursorLookupAgent
from .agents_media import SoundEffectsAgent
from .agents_trekcore import TrekCoreAgent
from .orchestrator import Orchestrator, Task
from .registry import AgentRegistry


def build_default_registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register("echo", lambda name, config=None: EchoAgent(name, config))
    registry.register("shell", lambda name, config=None: ShellAgent(name, config))
    registry.register("webget", lambda name, config=None: WebGetAgent(name, config))
    registry.register("cursor", lambda name, config=None: CursorLookupAgent(name, config))
    registry.register("sfx", lambda name, config=None: SoundEffectsAgent(name, config))
    registry.register("trekcore", lambda name, config=None: TrekCoreAgent(name, config))
    return registry


def _notify_macos(title: str, message: str) -> None:
    if sys.platform != "darwin":
        return
    try:
        import subprocess

        safe_title = title.replace("\"", r"\\\"")
        safe_msg = message.replace("\"", r"\\\"")
        script = f'display notification "{safe_msg}" with title "{safe_title}"'
        subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
    except Exception:
        pass


def _parse_tasks_from_stream(stream: TextIO) -> List[Dict[str, Any]]:
    data = stream.read()
    if not data.strip():
        return []
    try:
        loaded = json.loads(data)
        if isinstance(loaded, list):
            return loaded
        # Single task object
        return [loaded]
    except json.JSONDecodeError:
        # Try NDJSON lines
        tasks: List[Dict[str, Any]] = []
        for line in data.splitlines():
            line = line.strip()
            if not line:
                continue
            tasks.append(json.loads(line))
        return tasks


def _load_tasks(path: Optional[str], stdin_fallback: bool) -> List[Task]:
    raw_items: List[Dict[str, Any]] = []
    if path and path != "-":
        raw_items = json.loads(Path(path).read_text())
    else:
        if stdin_fallback or not sys.stdin.isatty():
            raw_items = _parse_tasks_from_stream(sys.stdin)
        else:
            raise SystemExit("No tasks provided. Use --tasks PATH or pipe JSON to stdin or pass --stdin.")

    tasks: List[Task] = []
    for item in raw_items:
        tasks.append(
            Task(
                id=str(item.get("id", "")),
                agent_type=item["agent_type"],
                input=item.get("input", {}),
                name=item.get("name"),
                config=item.get("config"),
            )
        )
    return tasks


def _run_subcommand(args: argparse.Namespace) -> int:
    registry = build_default_registry()
    orch = Orchestrator(registry)
    try:
        tasks = _load_tasks(args.tasks, args.stdin)
        results = orch.run_tasks(tasks)
        # Optional per-task file outputs
        if args.output_dir:
            out_dir = Path(args.output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            for item in results:
                task_id = item.get("task_id", "task")
                out_path = out_dir / f"{task_id}.json"
                out_path.write_text(json.dumps(item, indent=None if args.no_pretty else 2))
        print(json.dumps(results, indent=None if args.no_pretty else 2))
        if args.notify:
            _notify_macos("Synthos", f"Completed {len(results)} task(s)")
        return 0
    finally:
        orch.shutdown()


def _agent_subcommand(args: argparse.Namespace) -> int:
    registry = build_default_registry()
    orch = Orchestrator(registry)
    try:
        # Build a single Task
        if args.input == "-":
            input_payload = json.loads(sys.stdin.read())
        else:
            input_payload = json.loads(args.input)
        config_payload = json.loads(args.config) if args.config else None
        task = Task(
            id="single",
            agent_type=args.agent_type,
            input=input_payload,
            name=args.name,
            config=config_payload,
        )
        result = orch.run_task(task)
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(result, indent=None if args.no_pretty else 2))
        print(json.dumps(result, indent=None if args.no_pretty else 2))
        if args.notify:
            _notify_macos("Synthos", f"{args.agent_type} done")
        return 0
    finally:
        orch.shutdown()


def _repl_subcommand(args: argparse.Namespace) -> int:
    print("Synthos REPL. Enter lines like: 'echo {\"message\": \"hi\"}'")
    print("Commands: :q to quit, :help for help")
    registry = build_default_registry()
    orch = Orchestrator(registry)
    try:
        while True:
            try:
                line = input("synthos> ").strip()
            except EOFError:
                break
            if not line:
                continue
            if line in {":q", ":quit", ":exit"}:
                break
            if line in {":h", ":help", "help"}:
                print("Usage: <agent_type> <json_input>")
                print("Example: shell {\"command\": \"echo hi\"}")
                continue
            try:
                # Split first token as agent type, remainder as JSON
                parts = shlex.split(line, posix=True)
                if not parts:
                    continue
                agent_type = parts[0]
                json_str = line[len(parts[0]):].strip()
                if not json_str:
                    print("error: missing JSON payload")
                    continue
                payload = json.loads(json_str)
                task = Task(id="repl", agent_type=agent_type, input=payload)
                out = orch.run_task(task)
                print(json.dumps(out, indent=2))
            except Exception as exc:
                print(f"error: {exc}")
        return 0
    finally:
        orch.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthos CLI (macOS-optimized)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run tasks from a file or stdin")
    p_run.add_argument("--tasks", default=None, help="Path to JSON tasks file or '-' for stdin")
    p_run.add_argument("--stdin", action="store_true", help="Read tasks JSON from stdin")
    p_run.add_argument("--notify", action="store_true", help="macOS notification when done")
    p_run.add_argument("--no-pretty", action="store_true", help="Compact JSON output")
    p_run.add_argument("--output-dir", default=None, help="Directory to write per-task JSON results")
    p_run.set_defaults(func=_run_subcommand)

    p_agent = sub.add_parser("agent", help="Run a single agent once")
    p_agent.add_argument("agent_type", help="Registered agent type (e.g., echo, shell, webget)")
    p_agent.add_argument("--input", required=True, help="JSON string payload or '-' for stdin")
    p_agent.add_argument("--name", default=None, help="Optional agent instance name")
    p_agent.add_argument("--config", default=None, help="Optional JSON config for the agent")
    p_agent.add_argument("--notify", action="store_true", help="macOS notification when done")
    p_agent.add_argument("--no-pretty", action="store_true", help="Compact JSON output")
    p_agent.add_argument("--output", default=None, help="Write the single result JSON to this file path")
    p_agent.set_defaults(func=_agent_subcommand)

    # Convenience flags for cursor agent (optional sugar; still takes JSON input)
    # Example: synthos_core.cli agent cursor --input '{"query":"..."}' --cursor-lang en --cursor-max-pages 3 --cursor-markdown
    p_agent.add_argument("--cursor-lang", default=None, help="Convenience: language code for cursor agent")
    p_agent.add_argument("--cursor-max-pages", type=int, default=None, help="Convenience: max pages to scan")
    p_agent.add_argument("--cursor-markdown", action="store_true", help="Convenience: include markdown report in result")

    p_repl = sub.add_parser("repl", help="Interactive REPL for ad-hoc runs")
    p_repl.set_defaults(func=_repl_subcommand)

    args = parser.parse_args()
    code = args.func(args)
    raise SystemExit(code)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)


