def clean_file(filepath):
    try:
        # Read as text, which will replace null bytes with replacement character
        with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
        
        # Write back as clean text
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
            
        print(f"Cleaned {filepath}")
    except Exception as e:
        print(f"Error cleaning {filepath}: {e}")

files_to_clean = [
    'gui_components_cleaned.py',
    'gui/gui_components_cleaned.py',
    'gui/main_frame.py',
    'gui/token_section.py',
    'gui/backup_section.py',
    'gui/options_section.py',
    'gui/status_section.py',
    'gui/control_section.py'
]

for file in files_to_clean:
    clean_file(file)