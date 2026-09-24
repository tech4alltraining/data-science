import re

content = """
# Session 1 — Python Refresher

**Syntax · Comments · Variables · Data types · Numbers · Input & Output · Strings · Operators · Lists · Tuples & Sets · Dictionaries · Conditionals · Loops · Functions · Classes & Objects**

| | |
|---|---|
| **Notebook** | [session-01-python-refresher.ipynb](../notebooks/session-01-python-refresher.ipynb) |
| **Next** | [Session 2 — NumPy & Pandas](session-02-numpy-pandas.md) |
| **Stuck?** | [Troubleshooting](../troubleshooting.md) |

> **This session assumes you have never written a line of Python.** Every topic uses only what came before it. If something looks unfamiliar, it has not been taught yet — keep going in order and it will be.
"""

nav_table_pattern = re.compile(r"\|\s*\|\s*\|\n\|---\|---\|\n(?:\|.*?\|.*?\|\n)+", re.MULTILINE)
print("AFTER REPLACEMENT:")
print(nav_table_pattern.sub("", content))

