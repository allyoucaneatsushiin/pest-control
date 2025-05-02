import os
import csv

# Load city replacements from a CSV file
def load_city_mappings(csv_path):
    replacements = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                old, new = row[0].strip(), row[1].strip()
                replacements[old] = new
    return replacements

# Replace city names in a single file
def replace_in_file(file_path, replacements):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        updated = False
        for old_city, new_city in replacements.items():
            if old_city in content:
                content = content.replace(old_city, new_city)
                updated = True

        if updated:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Walk through all MD files and apply replacements
def process_all_md_files(folder_path, replacements):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                replace_in_file(full_path, replacements)

# === MAIN ===
if __name__ == "__main__":
    mappings_file = 'city_mappings.csv'  # Adjust if needed
    target_folder = '.'  # Adjust if your files are in another directory
    city_replacements = load_city_mappings(mappings_file)
    process_all_md_files(target_folder, city_replacements)
