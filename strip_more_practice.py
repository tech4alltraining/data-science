import os

path = "demos/"
for f in os.listdir(path):
    if f.endswith(".qmd"):
        filepath = os.path.join(path, f)
        with open(filepath, "r") as file:
            content = file.read()
        
        if "## More practice" in content:
            content = content.split("## More practice")[0]
            with open(filepath, "w") as file:
                file.write(content.strip() + "\n")
            print(f"Stripped {f}")
