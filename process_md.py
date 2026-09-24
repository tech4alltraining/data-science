import os, re

src_dir = "syllabus_files/md-files"
dst_dir = "demos"

os.makedirs(dst_dir, exist_ok=True)

md_files = [f for f in os.listdir(src_dir) if f.endswith(".md")]
# Sort files so we add them in a deterministic order later
md_files.sort()
md_names = [f[:-3] for f in md_files]

nav_table_pattern = re.compile(r"\|\s*\|\s*\|\n\|---\|---\|\n(?:\|.*?\|.*?\|\n)+", re.MULTILINE)

qmd_files = []
for f in md_files:
    src_path = os.path.join(src_dir, f)
    dst_path = os.path.join(dst_dir, f.replace(".md", ".qmd"))
    
    with open(src_path, "r") as src:
        content = src.read()
    
    # Remove navigation table
    content = nav_table_pattern.sub("", content)
    
    # Replace .md links with .qmd links for internal references
    for name in md_names:
        content = content.replace(name + ".md", name + ".qmd")
        
    with open(dst_path, "w") as dst:
        dst.write(content)
        
    qmd_files.append(f"demos/{f.replace('.md', '.qmd')}")

print("Created files:")
for q in qmd_files:
    print(f"        - {q}")
