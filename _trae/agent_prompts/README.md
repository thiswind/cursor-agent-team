# Agent Prompts — TRAE 智能体创建指南

本目录包含 cursor-agent-team 框架在 TRAE_CN 上运行所需的 **智能体提示词模板**。每个 `.md` 文件对应一个 TRAE 自定义智能体，需要手动在 TRAE GUI 中创建。

## 前提条件

- 已安装 TRAE_CN（v3.3.21+ / v1.3.0+）
- 已打开包含 `cursor-agent-team` 子模块的项目
- 已切换到 `trae-cn` 分支（`cd cursor-agent-team && git checkout trae-cn`）
- 已运行 `bash cursor-agent-team/install_trae.sh` 安装 Skills 和 Rules

## 智能体列表

本目录包含 3 个智能体提示词文件：

- `discussion_partner.md` — 讨论搭档（`discussion-partner`）
- `crew_member.md` — 执行组员（`crew-member`）
- `trae_prompt_engineer.md` — 提示工程师（`trae-prompt-engineer`）

每个文件顶部的 `## TRAE Form Fields` 区域包含在 TRAE GUI 中需要填写的字段值。

## 创建步骤（逐个智能体重复以下步骤）

### 第 1 步：打开智能体创建页面

TRAE → 右上角齿轮图标（设置）→ **智能体** 页签 → 点击 **+ 创建智能体**

### 第 2 步：填写「名称」

从提示词文件顶部 `## TRAE Form Fields` 区域复制 **Name** 字段的值。

例如：`讨论搭档`、`执行组员`、`提示工程师`

### 第 3 步：填写「提示词」

复制提示词文件中 **`## Agent Configuration` 及其以下的全部内容**，粘贴到「提示词」输入框。

> 注意：不要复制 `## TRAE Form Fields` 区域，只复制从 `## Agent Configuration` 开始到文件末尾的内容。

### 第 4 步：填写「英文标识名」

从 `## TRAE Form Fields` 区域复制 **Identifier** 字段的值。

例如：`discussion-partner`、`crew-member`、`trae-prompt-engineer`

### 第 5 步：填写「何时调用」

从 `## TRAE Form Fields` 区域复制 **When to Invoke** 字段的值。

### 第 6 步：配置工具

在「工具」区域启用以下内置工具：

- ✅ 文件系统
- ✅ 终端
- ✅ 联网搜索

### 第 7 步：点击「创建」

确认所有字段填写完毕后，点击底部的 **创建** 按钮。

## 使用方式

创建完成后，在 TRAE 对话输入框中输入 `@` 即可看到你的智能体：

- `@讨论搭档` — 讨论问题、分析方案、生成执行方案
- `@执行组员` — 严格按方案执行操作
- `@提示工程师` — 创建/修改智能体提示词和 Skills

## 注意事项

- **提示词字符限制**：TRAE 提示词字段最多 10000 字符，本目录三个文件均在限制内
- **SOLO Coder 调度**：填写「英文标识名」和「何时调用」后，SOLO Coder 可在 SOLO 模式下自动调度这些智能体
- **更新提示词**：当 `_trae/agent_prompts/` 中的文件更新后，需要手动重新粘贴到 TRAE GUI（设置 → 智能体 → 选中要修改的智能体 → 编辑）
- **Skills 和 Rules**：智能体创建是独立于 Skills/Rules 安装的，Skills/Rules 通过 `install_trae.sh` 安装到 `.trae/` 目录

---

**Version**: v1.0.0 (Created: 2026-02-27)
