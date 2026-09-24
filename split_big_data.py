import re

with open('syllabus_files/md-files/big-data.md', 'r') as f:
    content = f.read()

# Split at "# Part 6"
parts = re.split(r'(?=# Part 6 —)', content)

if len(parts) >= 2:
    part1 = parts[0]
    part2 = ''.join(parts[1:])
    
    with open('demos/session-06-big-data-part1.qmd', 'w') as f:
        f.write(part1)
        
    with open('demos/session-07-big-data-part2.qmd', 'w') as f:
        f.write(part2)
        
    print("Split successful!")
else:
    print("Could not find '# Part 6 —' to split at.")
