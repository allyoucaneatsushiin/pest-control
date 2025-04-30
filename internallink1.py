import os
import re
import random

DISCLAIMER = """*IMPORTANT **Disclaimer:**

This site [Github.com] is a free service to assist homeowners in connecting with local service providers. All contractors/providers are independent and [Github.com] does not warrant or guarantee any work performed. It is the responsibility of the homeowner to verify that the hired contractor furnishes the necessary license and insurance required for the work being performed. All persons depicted in a photo or video are actors or models and not contractors listed on this site [Github.com].
"""

def extract_city_service(filename):
    # e.g., "Backflow-Testing-Abbott-TX-..." -> ("Backflow Testing", "Abbott")
    parts = filename.replace('.md', '').split('-')
    if 'TX' in parts:
        tx_index = parts.index('TX')
        if tx_index >= 2:
            city = parts[tx_index - 1]
            service = ' '.join(parts[:tx_index - 1])
            return service.strip(), city.strip()
    return None, None

def keyword_from_filename(filename):
    # Create readable keyword for anchor text
    parts = filename.replace('.md', '').split('-')
    if 'TX' in parts:
        tx_index = parts.index('TX')
        if tx_index >= 2:
            city = parts[tx_index - 1]
            service = ' '.join(parts[:tx_index - 1])
            return f"{service} {city} TX"
    return filename.replace('.md', '')

def build_internal_links(current_file, service, city, all_pages_info, max_links=4):
    # Prioritize same city, then same service
    links = []

    # Filter same city (exclude self)
    same_city = [p for p in all_pages_info if p["city"] == city and p["filename"] != current_file]
    if len(same_city) >= max_links:
        links = same_city[:max_links]
    else:
        links.extend(same_city)
        remaining = max_links - len(links)
        same_service = [p for p in all_pages_info if p["service"] == service and p["filename"] != current_file and p not in links]
        links.extend(same_service[:remaining])

    # Build markdown links
    markdown_links = "\n".join([f"- [{p['keyword']}](https://github.com/allyoucaneatsushiin/plumbing-texas/blob/main/{p['filename']})" for p in links])
    return markdown_links

def process_markdown_files():
    all_files = [f for f in os.listdir('.') if f.endswith('.md')]
    all_pages_info = []

    for filename in all_files:
        service, city = extract_city_service(filename)
        if service and city:
            keyword = keyword_from_filename(filename)
            all_pages_info.append({
                "filename": filename,
                "service": service,
                "city": city,
                "keyword": keyword
            })

    for page in all_pages_info:
        file_path = page["filename"]
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove all old disclaimers (even multiple ones)
        content = re.sub(r"\*IMPORTANT\s+\*\*Disclaimer:.*?contractors listed on this site \[Github\.com\]\.\s*", "", content, flags=re.DOTALL)

        # Remove old disclaimer variants
        content = re.sub(r"\*\*Disclaimer:.*?contractors listed on this site \[Github\.com\]\.\s*", "", content, flags=re.DOTALL)

        # Remove old internal links section if exists
        content = re.sub(r"## Internal Links\s*- \[.*?\)\s*", "", content, flags=re.DOTALL)

        # Add disclaimer at the end
        content += f"\n\n{DISCLAIMER}\n"

        # Add internal links
        internal_links = build_internal_links(page["filename"], page["service"], page["city"], all_pages_info)
        if internal_links:
            content += f"\n## Internal Links\n{internal_links}\n"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Processed: {file_path}")

if __name__ == "__main__":
    process_markdown_files()
