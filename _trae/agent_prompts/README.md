# Agent Prompts — TRAE 智能体创建指南

本目录包含 cursor-agent-team 框架在 TRAE_CN 上运行所需的 **智能体提示词模板** 和 **创建指南**。

## 前提条件

- 已安装 TRAE_CN（v3.3.21+ / v1.3.0+）
- 已打开包含 `cursor-agent-team` 子模块的项目
- 已切换到 `trae-cn` 分支（`cd cursor-agent-team && git checkout trae-cn`）
- 已运行 `bash cursor-agent-team/install_trae.sh` 安装 Skills 和 Rules

## 智能体列表

每个智能体都有两个文件：**提示词文件**（Agent Prompt）和**创建指南**（INSTALL_GUIDE）。

### 讨论搭档（Discussion Partner）

- 提示词文件：[`discussion_partner.md`](discussion_partner.md)
- 创建指南：[`discussion_partner_INSTALL_GUIDE.md`](discussion_partner_INSTALL_GUIDE.md)
- 英文标识：`discussion-partner`

### 执行组员（Crew Member）

- 提示词文件：[`crew_member.md`](crew_member.md)
- 创建指南：[`crew_member_INSTALL_GUIDE.md`](crew_member_INSTALL_GUIDE.md)
- 英文标识：`crew-member`

### 提示工程师（TRAE Prompt Engineer）

- 提示词文件：[`trae_prompt_engineer.md`](trae_prompt_engineer.md)
- 创建指南：[`trae_prompt_engineer_INSTALL_GUIDE.md`](trae_prompt_engineer_INSTALL_GUIDE.md)
- 英文标识：`trae-prompt-engineer`

## 如何创建智能体

请打开对应智能体的 **INSTALL_GUIDE.md** 文件，按照其中的 7 步操作流程在 TRAE GUI 中创建智能体。每个 INSTALL_GUIDE 中已填好所有表单字段值，直接复制粘贴即可。

## 使用方式

创建完成后，在 TRAE 对话输入框中输入 `@` 即可看到你的智能体：

- `@讨论搭档` — 讨论问题、分析方案、生成执行方案
- `@执行组员` — 严格按方案执行操作
- `@提示工程师` — 创建/修改智能体提示词和 Skills

## 新智能体的创建

使用 `@提示工程师` 创建新智能体时，它会自动生成：
1. 提示词文件（`<name>.md`）
2. 创建指南（`<name>_INSTALL_GUIDE.md`）

## 注意事项

- **提示词字符限制**：TRAE 提示词字段最多 10000 字符
- **SOLO Coder 调度**：填写「英文标识名」和「何时调用」后，SOLO Coder 可自动调度智能体
- **更新提示词**：文件更新后需手动重新粘贴到 TRAE GUI
- **Skills 和 Rules**：通过 `install_trae.sh` 安装，与智能体创建独立

---

**Version**: v2.0.0 (Updated: 2026-02-27)
