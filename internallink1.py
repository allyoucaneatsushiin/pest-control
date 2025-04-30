import os
import re
import random

DISCLAIMER = """*IMPORTANT **Disclaimer:**  

This site [Github.com] is a free service to assist homeowners in connecting with local service providers. All contractors/providers are independent and [Github.com] does not warrant or guarantee any work performed. It is the responsibility of the homeowner to verify that the hired contractor furnishes the necessary license and insurance required for the work being performed. All persons depicted in a photo or video are actors or models and not contractors listed on this site [Github.com].
"""

def extract_city_service(filename):
    parts = filename.replace('.md', '').split('-')

    # Look for "TX", "AZ", etc. to identify the location and city
    state_identifiers = ['TX', 'AZ', 'NC', 'CA', 'NM', 'SD', 'IL']  # Add other states if needed
    for state in state_identifiers:
        if state in parts:
            tx_index = parts.index(state)
            city = parts[tx_index - 1]  # City is the part right before the state
            service = ' '.join(parts[:tx_index - 1])  # Everything before the city is the service name
            return service.strip(), city.strip()

    # If state wasn't found, fall back to default handling
    print(f"[⚠️ Skipped Parsing] Filename: {filename}")
    return "General Service", "Unknown City"

def keyword_from_filename(filename):
    parts = filename.replace('.md', '').split('-')
    if 'TX' in parts:
        tx_index = parts.index('TX')
        if tx_index >= 2:
            city = parts[tx_index - 1]
            service = ' '.join(parts[:tx_index - 1])
            return f"{service} {city} TX"
    return filename.replace('.md', '').replace('-', ' ')

def build_internal_links(current_file, service, city, all_pages_info, max_links=4):
    links = []

    same_city = [p for p in all_pages_info if p["city"] == city and p["filename"] != current_file]
    random.shuffle(same_city)

    if len(same_city) >= max_links:
        links = same_city[:max_links]
    else:
        links.extend(same_city)
        remaining = max_links - len(links)
        same_service = [p for p in all_pages_info if p["service"] == service and p["filename"] != current_file and p not in links]
        random.shuffle(same_service)
        links.extend(same_service[:remaining])

    markdown_links = "\n".join([
        f"- [{p['keyword']}](https://github.com/allyoucaneatsushiin/plumbing-texas/blob/main/{p['filename']})"
        for p in links
    ])
    return markdown_links

def process_markdown_files():
    all_files = [f for f in os.listdir('.') if f.endswith('.md')]
    all_pages_info = []

    for filename in all_files:
        service, city = extract_city_service(filename)
        keyword = keyword_from_filename(filename)
        all_pages_info.append({
            "filename": filename,
            "service": service,
            "city": city,
            "keyword": keyword
        })

    for page in all_pages_info:
        file_path = page["filename"]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove old disclaimers
            content = re.sub(
                r"\*?IMPORTANT\s+\*\*Disclaimer:.*?\[Github\.com\]\.\s*",
                "",
                content,
                flags=re.DOTALL
            )

            # Remove old internal links
            content = re.sub(
                r"## Internal Links\s*- \[.*?\)\s*",
                "",
                content,
                flags=re.DOTALL
            )

            # Append disclaimer and links
            content += f"\n\n{DISCLAIMER}\n"

            internal_links = build_internal_links(
                page["filename"], page["service"], page["city"], all_pages_info
            )
            if internal_links:
                content += f"\n## Internal Links\n{internal_links}\n"

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Processed: {file_path}")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    process_markdown_files()
