# _scripts - 框架级硬约束脚本

此目录存放框架级的硬约束验证脚本。这些脚本用于在 LLM 执行某些关键操作时提供确定性的验证，弥补 LLM 随机性可能导致的错误。

## 设计理念

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
│   - 验证输出格式                                │
│   - 检查必要字段                                │
│   - 返回错误时LLM重试                           │
└─────────────────────────────────────────────────┘
```

- **软约束（LLM层）**：通过提示词规则引导 LLM 行为，但无法 100% 保证遵守
- **硬约束（脚本层）**：通过确定性脚本验证输出，错误时返回明确信息让 LLM 修正

## 与 ai_workspace/ 的区别

| 目录 | 性质 | 创建者 | 生命周期 | Git跟踪 |
|:--|:--|:--|:--|:--|
| `_scripts/` | 框架基础设施 | 人类 | 持久 | ✅ 是 |
| `ai_workspace/` | LLM 临时工作区 | LLM | 临时 | ❌ 否 |

- `_scripts/` 中的脚本是框架的一部分，应该被版本控制
- `ai_workspace/` 中的文件是 LLM 的临时工作产物，可随时清理

## 脚本列表

### validate_topic_tree.py

**用途**：验证话题树更新是否符合硬约束规则

**验证规则**：
- **R1**: 所有历史话题ID必须保留（防止话题丢失）
- **R2**: 禁止使用"省略"/"..."等标记简化历史
- **R3**: 必须包含 Last Updated 字段
- **R4**: 状态值必须是预定义值之一（警告级别）

**使用方法**：

```bash
python _scripts/validate_topic_tree.py \
  --old ai_workspace/temp/discussion_topics.md.bak \
  --new ai_workspace/temp/new_topic_tree.md
```

**输出格式**（JSON）：

```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

或失败时：

```json
{
  "valid": false,
  "errors": ["R1违规: 以下话题ID丢失: ['A', 'B']"],
  "warnings": []
}
```

**退出码**：
- `0` - 验证通过（valid=true）
- `1` - 验证失败（valid=false）

### cleanup_topic_tree_temp.py

**用途**：清理话题树验证流程产生的临时文件

**安全机制**：
- **白名单限制**：只能删除预定义的文件名（硬编码）
- **路径限制**：只能操作 `ai_workspace/temp/` 目录
- **无任意路径暴露**：LLM 无法通过参数删除其他文件

**使用方法**：

```bash
# 基本用法：清理话题树临时文件
python cursor-agent-team/_scripts/cleanup_topic_tree_temp.py

# 预览模式：只显示将删除的文件，不实际删除
python cursor-agent-team/_scripts/cleanup_topic_tree_temp.py --dry-run

# 扩展清理：包括所有 .bak 和 .tmp 文件
python cursor-agent-team/_scripts/cleanup_topic_tree_temp.py --all

# 静默模式：不输出到终端（仍写日志）
python cursor-agent-team/_scripts/cleanup_topic_tree_temp.py --quiet
```

**参数说明**：

| 参数 | 说明 |
|:--|:--|
| `--dry-run` | 预览模式，只显示将删除的文件 |
| `--all` | 扩展清理，包括 *.bak 和 *.tmp |
| `--quiet` | 静默模式，不输出到终端 |

**输出格式**（JSON）：

```json
{
  "success": true,
  "deleted": ["discussion_topics.md.bak"],
  "skipped": [],
  "dry_run": false,
  "log_file": "ai_workspace/temp/cleanup.log"
}
```

**日志位置**：`ai_workspace/temp/cleanup.log`

**退出码**：
- `0` - 成功
- `1` - 失败

## 双缓冲验证流程

LLM 在更新话题树时应遵循以下流程：

1. **备份**：将当前话题树复制到 `ai_workspace/temp/discussion_topics.md.bak`
2. **生成**：将新内容写入 `ai_workspace/temp/new_topic_tree.md`
3. **验证**：调用验证脚本检查新内容
4. **处理结果**：
   - 验证通过 → 用新内容覆盖正式文件，删除临时文件
   - 验证失败 → 根据错误修正，重试验证
   - 连续失败3次 → 还原备份，向用户报告错误

## 添加新脚本

如需添加新的硬约束脚本，请遵循以下规范：

1. **输出格式**：统一使用 JSON 格式，包含 `valid`、`errors`、`warnings` 字段
2. **退出码**：成功返回 0，失败返回 1
3. **错误信息**：清晰描述违规的具体规则和内容
4. **文档更新**：在此 README 中添加脚本说明

## 版本历史

- **v1.1.0** (2026-02-01): 添加 cleanup_topic_tree_temp.py 清理脚本
- **v1.0.0** (2026-01-31): 初始版本，添加 validate_topic_tree.py
