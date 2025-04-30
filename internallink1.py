import os
import re

# Constants
OLD_REPO_BASE = "https://github.com/allyoucaneatsushiin/plumbing-texas/"
NEW_REPO_BASE = "https://github.com/allyoucaneatsushiin/pest-control/"

# Regex patterns
markdown_link_pattern = re.compile(r'\[([^\]]+)\]\((https://github\.com/allyoucaneatsushiin/plumbing-texas/.+?)\)')
valid_filename_pattern = re.compile(r'^([A-Za-z-]+-\d{3}-\d{3}-\d{4}-[A-Za-z-]+\.md)$')

# Process all .md files in the current directory
for filename in os.listdir():
    if not filename.endswith(".md"):
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_link(match):
        link_text = match.group(1)
        old_url = match.group(2)

        # Extract filename from old URL
        file_name = old_url.split("/")[-1]

        # Check if this file exists in current directory (i.e., pest-control repo)
        if os.path.isfile(file_name):
            new_url = NEW_REPO_BASE + "blob/main/" + file_name
            return f"[{link_text}]({new_url})"
        else:
            print(f"❌ Removing broken link in {filename}: {file_name}")
            return ''  # remove the link if file doesn't exist

    # Replace or remove links
    new_content, subs = markdown_link_pattern.subn(replace_link, content)

    # Save only if something changed
    if subs > 0:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated {subs} link(s) in: {filename}")
