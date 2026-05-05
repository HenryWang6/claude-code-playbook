# Markdown Previewer — Sample Page

## What this is

A **Markdown** to *HTML* converter built with Python and [mistune](https://github.com/lepture/mistune).

## Features

- Headings (h1 through h6)
- **Bold** and *italic* text
- Inline `code` snippets
- Fenced code blocks with syntax highlighting
- Links and images
- Ordered and unordered lists
- Blockquotes
- Tables

## Code Example

```python
#!/usr/bin/env python3

def greet(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
```

## A Quote

> The best way to predict the future is to invent it.
> — Alan Kay

## Task List

- [x] Set up Python venv
- [x] Install mistune
- [ ] Write the converter
- [ ] Test everything

## Data Table

| Name    | Version | Status  |
|---------|---------|---------|
| Python  | 3.11.7  | Active  |
| mistune | 3.2.1   | Active  |
| HTML    | 5       | Stable  |

### An Image

![A landscape photo](https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800)

## Nested List

1. First step
   - Detail A
   - Detail B
2. Second step
   1. Sub-step one
   2. Sub-step two
3. Done

---

*Generated with Claude Code + mistune*
