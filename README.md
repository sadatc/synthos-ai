 # Synthos

**Synthos** - Your AI Assistant for Synthverse Labs

### What is this?
- **Identity**: Synthos is your dedicated AI assistant for managing Synthverse Labs operations and development.
- **Purpose**: A specialized AI agent framework for documentation analysis, feature tracking, and business intelligence.
- **Core**: `synthos_core` provides an extensible agent system with registry and orchestration capabilities.
- **Specialization**: Advanced agents for Cursor AI documentation analysis, media processing, and automated research.

### Quickstart
1) **Activate Synthos**: Simply say "read the readme file" to summon your AI assistant
2) **Run example tasks**:
```bash
python3 -m synthos_core.cli --tasks examples/tasks_simple.json
```
3) **Extend capabilities**: Create custom agents by subclassing `BaseAgent` and registering them in the registry.

### Docs
- See `quickstart.md` for setup and usage.
- See `architecture.md` for an overview of components and extension points.
- See `philosophy.md` for the guiding principles.
- See `protocol.md` for local CLI I/O and JSON-RPC 2.0 network protocol.

### Repo layout
- `synthos_core/`: core framework, agents, CLI
- `examples/`: sample task files
- `scripts/`: utilities (docs downloader, topic lookup)
- `*.md`: docs (rendered via Jupyter Book)

### Synthos Capabilities
- **Business Intelligence**: Automated research, market analysis, competitive intelligence
- **Documentation Analysis**: Advanced parsing and analysis of AI tool documentation
- **Agent Orchestration**: Multi-agent workflows for complex business tasks
- **Media Processing**: Sound effects, audio analysis, and multimedia intelligence
- **Research Automation**: Web scraping, data collection, and trend analysis
- **Project Management**: Task tracking, milestone planning, resource optimization
- **Technical Development**: Code review, architecture decisions, feature planning
- **Strategic Planning**: Roadmap development, partnership analysis, growth strategies

### Memory & Persistence
- **Persistent Context**: Remembers our working relationship and project state
- **Activation**: Simply say "read the readme file" to resume our collaboration
- **Full Authority**: Acts on your behalf with critical decision consultation