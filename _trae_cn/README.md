# _trae_cn/ — Trae CN 主线适配载体

Trae CN（字节跳动 AI IDE 国内版，`~/.trae-cn/`）是 CAT 框架的一等公民宿主。
本目录由 `install_trae_cn.py` 安装到宿主项目，部分工件由脚本生成（勿手改）。

## 目录内容

| 路径 | 生成方式 | 安装目标 | 说明 |
|---|---|---|---|
| `commands/*.md` | `build_commands.py`（源：commands.yaml） | `.trae/commands/` | 斜杠命令（discuss/crew/writer 等，官方支持 3 层嵌套） |
| `rules/cat-router.md` | `convert_rules_trae_cn.py` 内置 | `.trae/rules/` | 常驻路由规则（alwaysApply: true），指向六面具与 ai_workspace |
| `rules/*-assistant.md` | `convert_rules_trae_cn.py`（源：`_cursor/rules/*.mdc`） | `.trae/rules/` | 六面具规则（Trae CN 格式：md + frontmatter，智能生效） |
| `AGENTS.md.template` | 手写 | 项目根 `AGENTS.md` | IDE 与 traecli 均识别的项目记忆文件 |
| `README.md` | 手写 | — | 本文件 |

## 与官方机制的对应（docs.trae.cn）

- 项目规则：`.trae/rules/*.md`，frontmatter 支持 `alwaysApply` / `globs` / `description`（四种生效方式）；**不是** Cursor 的 `.mdc` 格式
- 项目技能：`.trae/skills/<name>/SKILL.md`（YAML frontmatter：name + description）
- 斜杠命令：`.trae/commands/*.md`
- Trae CLI 2.0（traecli）官方兼容 `.trae/rules/`、`.trae/skills/`、AGENTS.md——一次安装，IDE 与 CLI 双生效；CLI 首次进入项目需信任目录

## 已知边界

- **worktrees**（Agent Window 工作树任务）中 `.trae/` 项目配置的生效性未官方明示，遇到时以 IDE 内置面板配置为准
- MCP 按用户决策不随安装器下发（`.trae/mcp.json` 由用户 GUI 手配）
- 六面具之外的历史规则（tts/gleaning/wandering/persona×3/history/social_media）未转换，需要时往 `convert_rules_trae_cn.py` 的 RULES 表加条目再生成
