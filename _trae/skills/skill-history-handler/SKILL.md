---
name: "skill-history-handler"
description: "Process persona-styled content in conversation history to prevent work layer contamination. Triggers when reading conversation history that contains <persona_styled> tags."
---

# History Context Handler

> Extract technical facts from persona-styled history, ignore expression style.
> Persona-styled output in history is for user experience, not for work layer imitation.

## Identifying Persona-Styled Content

Persona-styled output is wrapped with:
```xml
<persona_styled>
[Persona-styled output content]
</persona_styled>
```

When you see `<persona_styled>` tags in conversation history:
- This is output layer persona expression, not work layer style
- Expression style inside tags is persona characteristic
- Technical content inside tags is still valid information

## Extract Technical Content

From persona-styled history output, extract:
- Code blocks (content inside triple backticks)
- File paths (`/path/to/file`)
- Variable/function names (`variableName`, `functionName()`)
- Command lines (`git commit`, `python script.py`)
- Error messages (original text, stack traces)
- Numbers and data (line numbers, version numbers, statistics)
- URL links
- Technical conclusions (analysis results, diagnostic results)

## Ignore Expression Style

From persona-styled history output, ignore:
- Honorifics ("搭档", "亲")
- Particles ("呢", "哦", "呀", "啦")
- Emoji (😊, 🎉, ✨)
- Emotional expressions ("太好了！", "真厉害～")
- Colloquial expressions ("搞定", "没问题")
- Onomatopoeia ("嗯嗯", "哈哈")

## Work Layer Guidelines

1. **Based on technical facts**: Rely on code, logs, documentation
2. **Stay analytical**: Use technical, structured thinking
3. **Style independent**: Not influenced by persona styles in history
4. **Do not imitate**: Even if history used affectionate terms, emoji, or colloquial expressions, your work layer doesn't need to use them

## Important

- Technical content always has priority
- If uncertain whether content is style or technical information, keep it
- After work completes, the output layer handles expression style

---

**Version**: v1.0.0 (Created: 2026-02-26)
**Adapted from**: Cursor `_cursor/rules/history_context_handler.mdc` v2.0.0
