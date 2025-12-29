# AI工作空间（AI Workspace）

## 目录说明

本目录是AI在讨论过程中使用的"草稿本"工作空间。

## 用途

在 `/discuss` 命令模式下，AI可以在此目录中：
- **记录讨论笔记**：保存讨论要点和中间想法
- **编写临时脚本**：创建用于验证想法或处理数据的临时脚本
- **保存分析结果**：保存临时分析结果和计算过程
- **存储临时文件**：其他讨论过程中需要的临时文件

## 目录结构

```
ai_workspace/
├── scratchpad/          # AI的草稿本
│   ├── notes/          # 讨论笔记
│   ├── scripts/        # 临时脚本
│   ├── analysis/       # 临时分析结果
│   └── temp/           # 其他临时文件
└── README.md           # 本说明文档
```

## 使用规则

### 文件命名规范

- **笔记文件**：`note_YYYYMMDD_HHMMSS.md` 或 `note_[topic]_YYYYMMDD.md`
- **脚本文件**：`script_[purpose]_YYYYMMDD_HHMMSS.[ext]`
- **分析文件**：`analysis_[topic]_YYYYMMDD_HHMMSS.md`
- **临时文件**：`temp_[description]_YYYYMMDD_HHMMSS.[ext]`

### 使用范围

- **仅在 `/discuss` 模式下使用**：其他命令模式不使用此目录
- **临时性质**：文件是临时性的，可定期清理
- **人类可查看**：人类可以查看此目录，了解AI的思考过程

### 清理策略

- **保留期限**：建议保留最近7天的文件
- **清理方式**：可以手动清理，或设置自动清理脚本
- **重要内容**：如果讨论产生重要内容，应手动保存到 `discussions/` 或 `collaboration_outputs/`

## 与项目结构的关系

- **`00_meta/ai_workspace/`** - AI的临时工作空间（本目录）
- **`00_meta/collaboration_outputs/`** - 人类-AI协作的正式输出产物
- **各章节的 `discussions/`** - 具体章节的讨论记录

## 注意事项

1. **Git管理**：此目录默认被 `.gitignore` 排除（但 README 会被跟踪）
2. **隐私考虑**：确保不会意外暴露敏感信息
3. **版本控制**：临时文件不纳入版本控制
4. **人类审查**：人类可以随时查看AI的草稿本

---

**创建日期**：2025年12月29日

**最后更新**：2025年12月29日

