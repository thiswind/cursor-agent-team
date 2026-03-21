# OpenClaw 适配层（cursor-agent-team）

**最后更新**: 2026-03-21  

本目录包含跨平台安装脚本、Skills、模板与说明。**完整 CLI** 以 `python install.py --help` 为准。

---

## 系统要求

- **Python** 3.8+
- **OpenClaw CLI**：`openclaw` 在 `PATH`，版本满足 `install.py` 内检查（当前 **≥ 2026.2.6**）
- **OS**：Windows（PowerShell）、macOS、Linux；WSL 可选

---

## 安装（任意平台）

**与根 README 对齐（推荐）**：含 **「我是 Agent」**（标准 / 加速）与 **「我是 Human」** 的完整说明，见仓库根目录 [**README.md**](../README.md) 的 **「OpenClaw」** 一节。以下为 **Human** 侧命令摘要与平台示例。

在**已克隆的本仓库根目录下**进入本目录：

```bash
cd cursor-agent-team/_openclaw
python install.py -y
openclaw gateway restart
```

- **非交互**：`-y`；**默认**生成并非破坏同步 `ai_workspace` 到 OpenClaw workspace（框架运行时工作区必选）；若明确跳过，加 **`--no-ai-workspace`**。
- **仅预览**：`python install.py --dry-run --skip-openclaw-check`
- **安装会**：备份 `~/.openclaw/openclaw.json`，向 `skills.load.extraDirs` 写入本仓库 `_openclaw/skills` 的**绝对路径**，并按锚点合并 `AGENTS.md` / `SOUL.md`（见 `templates/`）。

**Windows PowerShell 示例**

```powershell
Set-Location path\to\cursor-agent-team\_openclaw
py -3 install.py -y
openclaw gateway restart
```

控制台编码问题可使用 Windows Terminal 或 `PYTHONIOENCODING=utf-8`。

### CLI 摘要（canonical）

| 项 | 说明 |
|----|------|
| `--merge` / `--apply-templates` | 合并模板（默认开） |
| `--no-merge` | 只更新 `openclaw.json`（若需） |
| `-y` | 非交互；**默认**同步 `ai_workspace` 到 workspace（可用 `--no-ai-workspace` 跳过） |
| `--ai-workspace` | 显式执行生成 + 同步（交互模式下也可用；与 `-y` 组合时常为冗余） |
| `--no-ai-workspace` | 跳过 `ai_workspace` 生成与同步（不推荐，除非确知不需要频道侧工作区） |
| `--force-ai-workspace` | 同步时覆盖 workspace 内已有种子文件（慎用） |
| `--dry-run` | 不写入 |
| `--skip-openclaw-check` | 跳过 openclaw 检测（测试/dry-run） |

### 单一事实来源：两处 `ai_workspace`

- 扩展目录旁的 `cursor-agent-team/ai_workspace`：`preflight_check.py` 相对路径行为见框架说明。
- 频道侧数据：以 **`$OPENCLAW_WORKSPACE/ai_workspace`** 为准，由 **`install.py` 同步策略** 填充，不会与扩展目录自动合并。

### json5

若 `openclaw.json` 非严格 JSON，需修复或安装可选 **`json5`**（见安装脚本报错提示）。

---

## 卸载（要点）

1. 编辑 `~/.openclaw/openclaw.json`（Windows：`%USERPROFILE%\.openclaw\openclaw.json`），从 `skills.load.extraDirs` 删除指向本仓库 `_openclaw/skills` 的项。  
2. 若不再需要本仓库的本地副本，可删除你的 clone 目录；若曾放在 OpenClaw 扩展目录下，可一并删除该副本。  
3. `openclaw gateway restart`  
4. 安装备份：`~/.openclaw/openclaw.json.backup.*` 可手动恢复。

---

## 自 Cursor 迁移到 OpenClaw（要点）

备份原项目 `ai_workspace` 后，复制到 `$OPENCLAW_WORKSPACE/ai_workspace`；脚本与路径以合并后的 `AGENTS.md` 为准。

---

## 安装后验证（用户）

1. `openclaw gateway restart`（若安装时尚未重启）。  
2. 频道发送 `/discuss` 做四阶段烟测（Phase Marker 来自 `phase_marker.py`）。  
3. 若安装时未同步或需补跑：`python install.py -y`（默认含 `ai_workspace`；跳过则用 `--no-ai-workspace`）。

---

## 自动化测试（可选）

`cursor-agent-team/_openclaw/tests/test_install_helpers.py` — 辅助函数单元测试。

---

## 常见问题

**找不到 `openclaw`？** 安装 OpenClaw 并将 CLI 加入 PATH。  

**私有仓库？** clone 需权限；安装逻辑不变。
