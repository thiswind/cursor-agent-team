# Cursor AI 智能体团队框架

一个用于 Cursor IDE 中 AI 辅助工作的三智能体协作系统。

## 概述

Cursor AI 智能体团队框架通过三个专门的智能体提供结构化的 AI 辅助工作方法：

- **`/discuss`** - 讨论伙伴：分析问题、探索想法、生成执行方案
- **`/prompt_engineer`** - 提示词工程师：创建和维护 LangGPT 格式的提示词模板
- **`/crew`** - 万能打工人：严格按照规范执行方案

## 特性

- **三智能体协作**：针对不同任务的专门智能体
- **AI 工作空间**：为 AI 智能体记录笔记、脚本和分析的专用工作空间
- **话题树管理**：自动跟踪讨论话题
- **方案生成**：从讨论中自动生成执行方案
- **工作空间隔离**：每个智能体都有自己独立的工作空间
- **时间感知**：始终考虑信息的时间性
- **学术优先搜索**：学术搜索优先使用顶级会议和期刊

## 安装

### 方法 1：直接复制

1. 将 `.cursor/` 目录复制到项目根目录
2. 将 `00_meta/` 目录复制到项目根目录
3. 确保项目结构遵循推荐的命名约定（见下文）

### 方法 2：Git 子模块（未来）

```bash
git submodule add https://github.com/thiswind/cursor-agent-team.git 00_meta/cursor-agent-team
```

## 目录结构

```
project-root/
├── .cursor/
│   ├── commands/
│   │   ├── discuss.md
│   │   ├── prompt_engineer.md
│   │   └── crew.md
│   └── rules/
│       ├── discussion_assistant.mdc
│       ├── prompt_engineer_assistant.mdc
│       └── crew_assistant.mdc
└── 00_meta/
    └── ai_workspace/
        ├── README.md
        ├── plans/
        │   └── README.md
        ├── prompt_engineer/
        │   └── README.md
        ├── crew/
        │   └── README.md
        └── scratchpad/
            ├── notes/
            ├── scripts/
            ├── analysis/
            └── temp/
```

## 工作目录命名建议

将本框架集成到项目中时，我们建议对实际工作目录使用编号前缀系统：

- `00_meta/` - 元数据和配置（框架位置）
- `01_*/` - 第一个主要工作部分
- `02_*/` - 第二个主要工作部分
- `03_*/` - 第三个主要工作部分
- ... 依此类推

此命名约定：
- 将元数据与实际工作分开
- 提供清晰的排序
- 便于识别每个目录的用途
- 与框架的 `00_meta/` 前缀配合良好

**示例结构：**
```
project-root/
├── 00_meta/              # 框架和元数据
│   ├── .cursor/          # 框架命令和规则
│   └── ai_workspace/     # AI 工作空间
├── 01_method/            # 方法部分
├── 02_experiments/       # 实验部分
├── 03_theory/            # 理论部分
└── ...
```

## 使用方法

### 使用 `/discuss`

讨论伙伴帮助您探索想法、分析问题并生成执行方案。

```bash
/discuss
黎曼度量学习的最新发展是什么？
```

准备生成执行方案时：
```bash
/discuss
讨论已经可以了，可以生成方案了
```

### 使用 `/prompt_engineer`

提示词工程师创建和维护 LangGPT 格式的提示词模板。

```bash
/prompt_engineer
我需要一个生成图表标题的提示词
```

### 使用 `/crew`

万能打工人执行由 `/discuss` 生成的方案。

```bash
/crew PLAN-E-001
```

或自动识别最新方案：
```bash
/crew
```

## 工作流程

1. **讨论**：使用 `/discuss` 探索想法并生成执行方案
2. **执行**：使用 `/crew` 执行方案，或使用 `/prompt_engineer` 处理提示词相关任务
3. **审查**：执行结果自动记录在讨论话题中

## 许可证

本项目采用 GNU 通用公共许可证 v3.0 (GPL-3.0) 许可。

详情请参阅 [LICENSE](LICENSE) 文件。

## 版本

当前版本：**v0.1.0**（第一个可用开发版）

版本历史请参阅 [CHANGELOG.md](CHANGELOG.md)。

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 作者

**thiswind**

- GitHub: [@thiswind](https://github.com/thiswind)

## 致谢

本框架是作为学术论文写作中人类-AI 协作研究项目的一部分开发的。

---

**注意**：这是第一个可用开发版本（v0.1.0）。框架功能正常，但可能有限制。欢迎反馈和贡献。

