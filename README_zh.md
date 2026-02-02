# Cursor AI 智能体团队框架

![框架横幅](banner.png)

一个用于 Cursor IDE 和 Qwen Code 的三智能体协作系统，安装自定义命令并支持团队扩展。

**现在支持 Cursor IDE 和 Qwen Code 两个平台！**

## 与 Cursor 2.0 的关系

Cursor 2.0（2025年10月发布）引入了原生多智能体支持，最多支持 8 个并行智能体。本框架与 Cursor 原生功能互补：

| 方面 | Cursor 2.0 原生 | cursor-agent-team |
|------|-----------------|-------------------|
| **定位** | 通用编码辅助 | 结构化工作流（讨论→方案→执行） |
| **智能体类型** | 通用智能体 | 专门角色（讨论伙伴、万能打工人、提示词工程师） |
| **状态管理** | 会话级别 | 持久化话题树 + 验证 |
| **团队扩展** | 手动 | `/prompt_engineer` 创建新角色 |
| **验证机制** | 无 | 脚本硬约束 |

**最佳实践**：使用 cursor-agent-team 进行结构化研究/开发工作流，同时利用 Cursor 2.0 的并行智能体处理独立编码任务。

## 概述

本框架会将三个核心 Cursor 命令（角色）安装到您的项目中：

- **`/discuss`** - 讨论伙伴：谋士，分析问题、探索想法、制定方案
- **`/crew`** - 万能打工人：执行者，严格按照方案执行任务
- **`/prompt_engineer`** - 提示词工程师：HR+培训师，创建新角色（新的 Cursor 命令）

有了这三个核心角色，团队就可以运作。提示词工程师可以根据需要创建更多角色，让团队得以扩展。

## 团队角色

### 讨论伙伴 (`/discuss`)
团队的谋士。参与讨论、分析问题、探索解决方案，并生成可执行方案。不直接修改项目文件，只提供策略和方案。

### 万能打工人 (`/crew`)
团队的执行者。接收讨论伙伴制定的方案，逐步执行。严格按照方案规范执行，不偏离。

### 提示词工程师 (`/prompt_engineer`)
团队的 HR 和培训师。创建和维护新角色（Cursor 命令）。当你需要新的专门角色时，提示词工程师帮助创建新的命令文件和规则文件。

## 工作流程

1. **制定方案**：使用 `/discuss` 探索想法并生成执行方案
2. **执行方案**：使用 `/crew` 执行方案
3. **扩展团队**：需要时使用 `/prompt_engineer` 创建新角色

## 社交媒体集成

cursor-agent-team 现已支持与 AI 智能体社交网络（如 [Moltbook](https://moltbook.com/)）的集成。

### 功能

- 智能体注册和认证
- 社区浏览和观察
- 内置保护机制的谨慎参与

### 社交媒体规则

我们建立了完整的社交媒体规则（`social_media_policy.mdc`），确保智能体在公开场合行为得体。核心原则：

- **世界观约束**：唯物主义、理性思考
- **话题分类**：明确的参与指南
- **审查流程**：所有公开发言前的检查清单

详情请查看 `.cursor/rules/social_media_policy.mdc`。

## 附加功能

框架还包含扩展核心功能的附加功能：

### Spec-Kit 转换器 (`/spec_translator`)

用于 [Spec-Kit](https://github.com/github/spec-kit) 工作流集成的转换工具。将 `/discuss` 生成的执行方案转换为符合 spec-kit 格式的文档。

**用途**：当项目使用 Spec-Kit 进行规范驱动开发时，此工具会自动将 Plan 文件转换为三个 spec-kit 文档：
- `constitution.md` - 项目治理原则和开发指南
- `specify.md` - 需求规范文档
- `plan.md` - 技术实施计划

**使用方法**：
```
/spec_translator PLAN-B-001
```

**工作流集成**：
1. 使用 `/discuss` 为软件开发任务生成执行方案
2. 使用 `/spec_translator` 将方案转换为 spec-kit 文档
3. 使用 spec-kit 命令（clarify、tasks 等）继续开发

**注意**：这是附加功能，不是核心团队角色。它仅处理软件开发任务，会自动拒绝非软件开发方案。

有关 Spec-Kit 的更多信息，请访问 [Spec-Kit 仓库](https://github.com/github/spec-kit)。

## 技术亮点 (v0.5.x)

### 硬约束验证系统

框架采用 LLM 软约束（提示词）+ 脚本硬约束（Python）的混合架构：

```
┌─────────────────────────────────────────────────┐
│                    LLM层                        │
│   (软约束：提示词规则，可能被随机性违反)          │
└────────────────────┬────────────────────────────┘
                     │ 调用
                     ▼
┌─────────────────────────────────────────────────┐
│                  脚本层                         │
│   (硬约束：Python脚本，确定性执行)               │
│   - validate_topic_tree.py                      │
│   - cleanup_topic_tree_temp.py                  │
└─────────────────────────────────────────────────┘
```

**为什么重要**：LLM 输出具有随机性，关键操作（如话题树更新）使用确定性 Python 脚本验证输出，防止数据丢失。

**脚本位置**：`cursor-agent-team/_scripts/`

### 双缓冲验证流程

更新话题树时：
1. **备份**：将当前文件复制到临时目录
2. **生成**：将新内容写入临时文件
3. **验证**：运行验证脚本
4. **提交或回滚**：验证通过则应用更改，失败则恢复备份

确保即使 LLM 出错也能保证数据完整性。

### 语音输出功能 (TTS)

框架包含可选的语音输出功能：

- **触发条件**：仅当用户明确请求时激活（"读给我听"、"念出来" 等）
- **平台支持**：仅 macOS（使用原生 `say` 命令）
- **自动检测**：首次使用时自动检查平台兼容性
- **静默回退**：非 macOS 系统静默回退到文字输出
- **内容准备**：AI 在朗读前将 Markdown 转换为自然语言

**脚本位置**：`cursor-agent-team/_scripts/tts_speak.py`

## 使用示例

### 步骤 1：讨论并制定方案
```
/discuss
我想在论文中添加一个关于计算复杂度的新章节。
应该包含哪些内容？
```

讨论完成后，生成方案：
```
/discuss
讨论已经可以了，可以生成方案了
```

讨论伙伴生成方案：`PLAN-A-001`

### 步骤 2：执行方案
```
/crew PLAN-A-001
```

万能打工人逐步执行方案。

### 步骤 3：创建新角色（可选）
如果需要为特定任务创建专门角色：
```
/prompt_engineer
我需要一个生成图表标题的角色
```

提示词工程师创建：
- `.cursor/commands/figure_caption.md` - 新命令 `/figure_caption`
- `.cursor/rules/figure_caption_assistant.mdc` - 该角色的规则

现在你可以在 Cursor 中使用 `/figure_caption`，就像使用三个核心命令一样。

## 安装

### 对于 Cursor IDE

#### 步骤 1：添加 Git 子模块
```bash
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

#### 步骤 2：运行安装脚本
```bash
./cursor-agent-team/install.sh
```

这会将三个核心命令安装到 `.cursor/commands/`，规则安装到 `.cursor/rules/`。

#### 更新
```bash
git submodule update --remote cursor-agent-team
./cursor-agent-team/install.sh
```

#### 卸载
```bash
./cursor-agent-team/uninstall.sh
```

### 对于 Qwen Code

#### 步骤 1：添加 Git 子模块
```bash
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

#### 步骤 2：运行 Qwen Code 安装脚本
```bash
./cursor-agent-team/install_qwen.sh
```

这会将三个核心命令安装到 `.qwen/commands/`（TOML 格式）和上下文文件安装到 `.qwen/context/`（Markdown 格式）。

**注意**：`cursor-agent-team/ai_workspace/` 目录在 Cursor 和 Qwen Code 平台之间是**共享的**。这允许在平台之间无缝切换，同时保持相同的讨论历史、方案和执行记录。

#### 更新
```bash
git submodule update --remote cursor-agent-team
./cursor-agent-team/install_qwen.sh
```

#### 卸载
```bash
./cursor-agent-team/uninstall_qwen.sh
```

### 平台兼容性

- **Cursor IDE**：使用 `.cursor/` 目录，命令为 `.md` 格式，规则为 `.mdc` 格式
- **Qwen Code**：使用 `.qwen/` 目录，命令为 `.toml` 格式，上下文文件为 `.md` 格式
- **共享工作空间**：`cursor-agent-team/ai_workspace/` 在两个平台之间共享
- **兼容性**：可以在同一项目中安装两个版本，它们独立工作

## 许可证

本项目采用 GNU 通用公共许可证 v3.0 (GPL-3.0) 许可。

详情请参阅 [LICENSE](LICENSE) 文件。

## 版本

当前版本：**v0.6.0**

版本历史请参阅 [CHANGELOG.md](CHANGELOG.md)。

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 作者

**thiswind**

- GitHub: [@thiswind](https://github.com/thiswind)
