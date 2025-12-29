# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-12-29

### Changed

- **Documentation refactoring**: Restructured README to clarify project as a Cursor IDE extension framework
- Clarified that `install.sh` installs commands into `.cursor/` directory, making them available as `/discuss`, `/prompt_engineer`, and `/crew` in Cursor
- Emphasized that `prompt_engineer` creates new roles (new Cursor commands), not just prompt templates
- Simplified documentation to focus on team roles and collaboration workflow
- Removed detailed feature lists, focusing on core concepts and usage examples
- Added complete examples showing how new roles are created as command files

## [0.1.0] - 2025-12-29

### Added

- Initial release of Cursor AI Agent Team Framework
- Three agents: discuss, prompt_engineer, crew
- AI workspace structure and templates
- Documentation (English and Chinese)
- Topic tree management system
- Plan generation functionality
- Workspace isolation for each agent
- Time-aware information retrieval
- Academic-first search strategy

### Features

- `/discuss` command: Discussion partner for exploring ideas and generating plans
- `/prompt_engineer` command: Prompt engineer for creating and maintaining LangGPT-formatted prompts
- `/crew` command: Crew member for executing plans strictly according to specifications
- AI workspace with dedicated directories for each agent
- Automatic discussion topic tracking
- Execution plan generation from discussions
- Research and document reading before execution

---

[0.1.1]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.1.1
[0.1.0]: https://github.com/thiswind/cursor-agent-team/releases/tag/v0.1.0
