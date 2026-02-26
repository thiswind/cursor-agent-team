# 提示工程师 — TRAE 创建指南

## 表单字段速查

以下是在 TRAE GUI 中创建「提示工程师」智能体时需要填写的所有字段值。

### 名称

```
提示工程师
```

### 提示词

复制 `trae_prompt_engineer.md` 中 **`## Agent Configuration`** 及以下的全部内容，粘贴到提示词输入框。

> 提示词文件路径：`cursor-agent-team/_trae/agent_prompts/trae_prompt_engineer.md`

### 英文标识名

```
trae-prompt-engineer
```

### 何时调用

```
当需要创建或修改智能体提示词、Skills、项目规则时调用。包括：新建Agent Prompt、更新SKILL.md文件、维护project_rules.md、以及对现有提示词进行迭代优化。此智能体采用交互式工作流，通过多轮对话确认需求后生成内容。
```

### 工具

- ✅ 文件系统
- ✅ 终端
- ✅ 联网搜索

---

## 创建步骤

1. 打开 TRAE → 右上角齿轮图标（设置）→ **智能体** 页签 → 点击 **+ 创建智能体**
2. 在「名称」字段输入：`提示工程师`
3. 在「提示词」字段粘贴 `trae_prompt_engineer.md` 中 `## Agent Configuration` 及以下的全部内容
4. 在「英文标识名」字段输入：`trae-prompt-engineer`
5. 在「何时调用」字段粘贴上方「何时调用」区域的完整文本
6. 在「工具」区域勾选：文件系统、终端、联网搜索
7. 点击 **创建**

---

## 使用方式

创建完成后，在 TRAE 对话输入框中输入 `@提示工程师` 即可调用。

---

**Version**: v1.0.0 (Created: 2026-02-27)
