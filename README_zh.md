# Cursor AI 智能体团队框架

一个用于 Cursor IDE 中 AI 辅助工作的三智能体协作系统。

## 概述

本框架提供三个核心团队角色，协同工作：

- **`/discuss`** - 讨论伙伴：谋士，分析问题、探索想法、制定方案
- **`/crew`** - 万能打工人：执行者，严格按照方案执行任务
- **`/prompt_engineer`** - 提示词工程师：HR+培训师，创建和维护新角色（提示词模板）

有了这三个核心团队角色，团队就可以运作并扩展。

## 团队角色

### 讨论伙伴 (`/discuss`)
团队的谋士。参与讨论、分析问题、探索解决方案，并生成可执行方案。不直接修改项目文件，只提供策略和方案。

### 万能打工人 (`/crew`)
团队的执行者。接收讨论伙伴制定的方案，逐步执行。严格按照方案规范执行，不偏离。

### 提示词工程师 (`/prompt_engineer`)
团队的 HR 和培训师。创建和维护新角色（LangGPT 格式的提示词模板）。当你需要新的专门角色时，提示词工程师帮助创建。

## 工作流程

1. **制定方案**：使用 `/discuss` 探索想法并生成执行方案
2. **执行方案**：使用 `/crew` 执行方案
3. **扩展团队**：需要时使用 `/prompt_engineer` 创建新角色

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
我需要一个生成图表标题的提示词
```

提示词工程师创建新的角色模板，供后续使用。

## 安装

### 步骤 1：添加 Git 子模块
```bash
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

### 步骤 2：运行安装脚本
```bash
./cursor-agent-team/install.sh
```

### 更新
```bash
git submodule update --remote cursor-agent-team
./cursor-agent-team/install.sh
```

### 卸载
```bash
./cursor-agent-team/uninstall.sh
```

## 许可证

本项目采用 GNU 通用公共许可证 v3.0 (GPL-3.0) 许可。

详情请参阅 [LICENSE](LICENSE) 文件。

## 版本

当前版本：**v0.1.0**

版本历史请参阅 [CHANGELOG.md](CHANGELOG.md)。

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 作者

**thiswind**

- GitHub: [@thiswind](https://github.com/thiswind)

---

**注意**：这是第一个可用开发版本（v0.1.0）。框架功能正常，但可能有限制。欢迎反馈和贡献。
