# cursor-agent-team — TRAE SOLO 适配说明

TRAE SOLO（字节跳动）平台适配版本。将 cursor-agent-team 的单人多角色 AI 协作方法论从 Cursor IDE 迁移到 TRAE SOLO。

## 前提条件

- TRAE SOLO 最新版本
- Python 3.8+
- Git
- 使用 main 分支，TRAE SOLO 适配已包含在内

## 安装

### 1. 在已有项目中添加子模块

与 Cursor 版相同：在已有项目根目录将 cursor-agent-team 作为子模块加入。若项目是 clone 且已带 `--recurse-submodules`，则已有 `cursor-agent-team` 目录，可跳过本步。

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

### 2. 运行安装脚本

```bash
python cursor-agent-team/install_trae_solo.py
```

脚本会：
- 在项目根目录创建 `.trae/skills/` 目录
- 将技能文件复制到 `.trae/skills/` 目录
- 将 `AGENTS.md` 模板复制到项目根目录
- 生成 `ai_workspace`（如果配置文件存在）

### 3. 在 TRAE SOLO 中配置

#### 启用 AGENTS.md
1. 前往 TRAE SOLO 设置 > 规则
2. 在导入设置处，打开"将 AGENTS.md 包含在上下文中"开关

#### 创建斜杠命令（推荐）
虽然 TRAE SOLO 没有直接从目录复制命令的功能，但你可以手动创建：
1. 前往 TRAE SOLO 设置 > 命令
2. 点击"创建"按钮
3. 配置以下命令（可参考 `_trae_solo/commands/` 目录中的模板）：
   - `/discuss`: 讨论搭档
   - `/crew`: 执行组员
   - `/prompt_engineer`: 提示工程师

#### 使用技能
- 技能已安装在 `.trae/skills/` 目录
- TRAE SOLO 会自动识别这些技能
- 你可以在对话中手动调用或让 AI 自动调用相关技能

### 4. 开始使用

现在你可以在 TRAE SOLO 中使用 Cursor Agent Team 的功能了：
- 使用技能：`cursor-agent-team-discuss`、`cursor-agent-team-crew`、`cursor-agent-team-prompt-engineer`
- 或使用斜杠命令（如果已创建）：`/discuss`、`/crew`、`/prompt_engineer`

注意：`ai_workspace` 目录在 Cursor 和 TRAE SOLO 之间共享，你可以在两个平台之间无缝切换工作。

## 使用方式

典型用法是多角色协作：讨论与执行分离、方案驱动。下面按三条常见流程举例。

### 流程一：讨论 → 出方案 → 执行

先和**讨论搭档**分析需求、定步骤并生成执行方案（如 `ai_workspace/plans/PLAN-XX-001.md`），再让**执行组员**按该方案逐步执行。让执行组员执行时，可说「执行」或「/crew PLAN-XX」（如 PLAN-AC-001），或在指令里写一段简短的方案要点。

```
@讨论搭档 我想做 XXX 功能/重构，先一起分析一下可行性和步骤，然后生成一份可执行的方案
（方案生成后）
@执行组员 执行 ai_workspace/plans/PLAN-XX-001.md
```

### 流程二：讨论 → 定需求/方案 → 提示工程师建新角色

先和**讨论搭档**确定新角色的职责、边界与流程，产出 AGENT-REQUIREMENT 或方案；再让**提示工程师**根据该文档生成 Agent 提示词与 INSTALL_GUIDE。

```
@讨论搭档 我需要一个用于 YYY 场景的新智能体，我们先把职责、边界和流程定下来，出一份 AGENT-REQUIREMENT
（需求/文档确定后）
@提示工程师 根据刚才和讨论搭档确定的 AGENT-REQUIREMENT（或 ai_workspace/agent_requirements/ 里的文件），生成新智能体的提示词和 INSTALL_GUIDE
```

### 流程三：小改现有提示词

先和**讨论搭档**确认要改什么、改到什么程度；再让**提示工程师**按结论修改对应文件。

```
@讨论搭档 我想在讨论搭档的提示词里增加对 Z 场景的说明，你帮我看下该怎么表述、改哪一段
（结论明确后）
@提示工程师 按刚才讨论的结论，在讨论搭档的提示词里增加对 Z 场景的说明
```

三个智能体也可单独用于简单询问或小改，但完整任务建议按上述流程多角色协作。

## 目录结构

```
cursor-agent-team/
├── _trae_solo/                      # TRAE SOLO 专用配置
│   ├── commands/                     # 命令配置
│   │   ├── crew.md
│   │   ├── discuss.md
│   │   └── prompt_engineer.md
│   ├── skills/                       # 技能配置
│   │   ├── cursor-agent-team-crew/
│   │   ├── cursor-agent-team-discuss/
│   │   └── cursor-agent-team-prompt-engineer/
│   ├── test_ai_workspace_access.py   # 测试脚本
│   └── test_system_stability.py      # 测试脚本
├── _cursor/                          # Cursor 专用
├── _scripts/                         # 共用脚本（两平台通用）
├── ai_workspace/                     # 共用工作区（两平台通用）
├── install.py                        # 安装脚本
└── TRAE_SOLO_README.md               # 本文件
```

## 与 Cursor 版本的区别

| 维度 | Cursor | TRAE SOLO |
|------|--------|-----------|
| 角色唤起 | `/discuss`、`/crew`、`/prompt_engineer` 命令 | `@讨论搭档`、`@执行组员`、`@提示工程师` 智能体 |
| 规则注入 | Cursor 自动注入 `.mdc` 文件 | TRAE SOLO 按需加载 Skills |
| 智能体创建 | 在 `.cursor/commands/` 中定义 | 在 GUI 中配置或直接使用 |
| 脚本 | 相同 | 相同 |
| AI 工作区 | 相同 | 相同 |

## 共享工作空间

TRAE SOLO 与 Cursor 共用同一个 `ai_workspace` 目录，实现：
- 同一套工作空间结构
- 同一套脚本和工具
- 数据在编辑器切换后保持一致
- 系统稳定性良好

## 测试与验证

可以运行以下测试脚本来验证系统稳定性：

```bash
python cursor-agent-team/_trae_solo/test_ai_workspace_access.py
python cursor-agent-team/_trae_solo/test_system_stability.py
```

## 更新

拉取 cursor-agent-team 更新后重新运行安装脚本：

```bash
git submodule update --remote cursor-agent-team && python cursor-agent-team/install.py
```

---

**版本**：v1.0.0（更新于 2026-04-07）。TRAE SOLO 适配已包含在内，安装请按上述说明操作。