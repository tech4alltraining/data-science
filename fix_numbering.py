import os, re

path = "demos/"
files = [f for f in os.listdir(path) if f.endswith(".qmd")]

# Matches things like "# 1. Heading" or "## 1.1 Heading" or "## 11.2 Load the Dataset"
heading_pattern = re.compile(r"^(#+)\s+\d+(?:\.\d+)*\.?\s+(.*)")
# Links like (#1-heading) or (#11-activate-the-conda-environment)
link_pattern = re.compile(r"\(#\d+(?:-\d+)*-(.*?)\)")

for f in files:
    filepath = os.path.join(path, f)
    with open(filepath, "r") as file:
        lines = file.readlines()
        
    in_code_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            
        if not in_code_block:
            match = heading_pattern.match(line)
            if match:
                print(f"{filepath}: Heading changed: {line.strip()} -> {match.group(1)} {match.group(2)}")
                lines[i] = f"{match.group(1)} {match.group(2)}\n"
            
            if link_pattern.search(lines[i]):
                new_line = link_pattern.sub(r"(#\1)", lines[i])
                if lines[i] != new_line:
                    print(f"{filepath}: Link changed: {lines[i].strip()} -> {new_line.strip()}")
                lines[i] = new_line
                
    with open(filepath, "w") as file:
        file.writelines(lines)
