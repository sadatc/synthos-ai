from __future__ import annotations

import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .agent import BaseAgent
from .memory import AgentMemory


USER_AGENT = "SynthosTrekCoreAgent/0.1 (+https://github.com/Syntvherse-Labs/synthos)"
REQUEST_TIMEOUT_SECONDS = 15
REQUEST_DELAY_SECONDS = 0.25
TREKCORE_AUDIO_ROOT = "https://www.trekcore.com/audio/"


def _http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        return resp.read()


def _extract_links(html_bytes: bytes, base_url: str) -> List[str]:
    html_text = html_bytes.decode(errors="replace")
    links: List[str] = []
    for m in re.finditer(r"href=\"([^\"]+)\"|href='([^']+)'", html_text, flags=re.I):
        href = m.group(1) or m.group(2)
        if not href:
            continue
        links.append(urllib.parse.urljoin(base_url, href))
    return links


def _list_categories() -> List[Tuple[str, str]]:
    # Returns list of (name, url) derived from any link under /audio/<category>/...
    root = TREKCORE_AUDIO_ROOT
    html_bytes = _http_get(root)
    links = _extract_links(html_bytes, root)
    categories = set()
    root_path = urllib.parse.urlparse(root).path
    for l in links:
        if not l.startswith(root):
            continue
        path = urllib.parse.urlparse(l).path
        if not path.startswith(root_path):
            continue
        rel = path[len(root_path):]  # e.g., 'aliensounds/x.mp3' or 'background/'
        parts = [p for p in rel.split('/') if p]
        if not parts:
            continue
        cat = parts[0]
        # Skip obvious non-categories if any
        if cat.lower() in {"images", "css", "js"}:
            continue
        categories.add(cat)
    out: List[Tuple[str, str]] = []
    for cat in sorted(categories):
        url = urllib.parse.urljoin(root, f"{cat}/")
        name = cat.replace('_', ' ').replace('-', ' ').title()
        out.append((name, url))
    return out


def _list_category_audio(category_url: str) -> List[str]:
    # Crawl given category page for audio links
    html_bytes = _http_get(category_url)
    links = _extract_links(html_bytes, category_url)
    audio_exts = [".mp3", ".wav", ".aiff", ".m4a", ".ogg"]
    audio: List[str] = []
    for l in links:
        path = urllib.parse.urlparse(l).path.lower()
        if any(path.endswith(e) for e in audio_exts):
            audio.append(l)
    return sorted(set(audio))


class TrekCoreAgent(BaseAgent):
    """
    Wrapper agent for TrekCore Audio [https://www.trekcore.com/audio/].

    Modes (input.action):
      - "list_categories": returns available major categories
      - "list_audio": requires input.category_url; returns audio links
      - "download": requires input.category_url; downloads audio to storage_dir
    """

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(name, config)
        self.memory = AgentMemory()
        self.storage_dir = Path(self.config.get("storage_dir", ".data/trekcore"))

    def run(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        action = task_input.get("action", "list_categories")
        if action == "list_categories":
            cats = _list_categories()
            # Remember category list snapshot
            self.memory.remember(self.name, key="trekcore_categories", value=str(len(cats)), tags="trekcore")
            return {"categories": [{"name": n, "url": u} for n, u in cats]}

        if action == "list_audio":
            category_url = task_input.get("category_url")
            if not category_url:
                return {"error": "missing 'category_url'"}
            audio = _list_category_audio(category_url)
            return {"category_url": category_url, "count": len(audio), "audio_urls": audio}

        if action == "download":
            category_url = task_input.get("category_url")
            if not category_url:
                return {"error": "missing 'category_url'"}
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            audio = _list_category_audio(category_url)
            downloaded: List[str] = []
            for a in audio:
                try:
                    data = _http_get(a)
                    name = Path(urllib.parse.urlparse(a).path).name or "audio.bin"
                    out_path = self.storage_dir / name
                    out_path.write_bytes(data)
                    downloaded.append(str(out_path))
                    self.memory.record_download(agent=self.name, url=a, category=category_url, filename=name, path=str(out_path))
                    time.sleep(REQUEST_DELAY_SECONDS)
                except Exception:
                    continue
            return {"category_url": category_url, "downloaded_count": len(downloaded), "files": downloaded}

        return {"error": f"unknown action: {action}"}


