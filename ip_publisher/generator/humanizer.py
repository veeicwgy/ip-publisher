from __future__ import annotations

import re


REPLACEMENTS = (
    ("首先", "先"),
    ("其次", "再看"),
    ("最后", "最后一层"),
    ("总的来说", "说到底"),
    ("值得注意的是", "要注意的一点是"),
    ("可以先", "先"),
    ("围绕", "关于"),
    ("需要注意", "要注意"),
)


def humanize_markdown(text: str) -> str:
    """Lightweight post-process inspired by Humanizer-zh principles."""

    result = text
    for source, target in REPLACEMENTS:
        result = result.replace(source, target)
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r"([。！？])([^\n#\-|>` ])", r"\1\n\2", result)
    result = re.sub(r"[ \t]+\n", "\n", result)
    return result.strip() + "\n"
