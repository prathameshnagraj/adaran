import json

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_slugs(url):
    parts = url.split('/')
    slugs = [part for part in parts if part and '.' not in part and not part.startswith('http')]
    return slugs

def detect_sitemap(url):
    if 'jindal.utdallas.edu' in url:
        return 'Jindal'
    elif 'accounting.utdallas.edu' in url:
        return 'Accounting'
    elif 'execed.utdallas.edu' in url:
        return 'Executive Education'
    elif 'fin.utdallas.edu' in url:
        return 'Finance'
    elif 'infosystems.utdallas.edu' in url:
        return 'Information Systems'
    elif 'marketing.utdallas.edu' in url:
        return 'Marketing'
    elif 'mba.utdallas.edu' in url:
        return 'MBA'
    elif 'om.utdallas.edu' in url:
        return 'Operations Management'
    elif 'osim.utdallas.edu' in url:
        return 'Organizations, Strategy & International Management'
    else:
        return 'Other'

def detect_program_type(url):
    url = url.lower()

    if '/mba' in url:
        return 'MBA'
    elif '/ms-' in url:
        return 'MS'
    elif '/bs-' in url or '/undergraduate' in url:
        return 'Undergraduate/BS'
    elif '/phd' in url:
        return 'PhD'
    elif '/execed' in url:
        return 'Executive Education'
    elif '/certificate' in url:
        return 'Certificate Program'
    elif '/honors' in url:
        return 'Honors Program'
    else:
        return 'Other'

def tag_metadata(data):
    tagged = []
    for entry in data:
        url = entry.get('url', '')
        text = entry.get('text', '')
        
        tagged_entry = {
            "source_url": url,
            "content_type": "webpage",
            "slugs": generate_slugs(url),
            "sitemap": detect_sitemap(url),
            "program_type": detect_program_type(url),
            "text": text  # Keeping original text for vector embedding
        }
        tagged.append(tagged_entry)
    
    return tagged

if __name__ == "__main__":
    # Input and output file paths
    input_path = "data_cleaned/cleaned_pages.json"
    output_path = "data_cleaned/tagged_pages.json"

    # Load -> Tag -> Save
    data = load_data(input_path)
    tagged_data = tag_metadata(data)
    save_data(tagged_data, output_path)

    print(f"✅ Metadata tagging complete! Tagged {len(tagged_data)} records. Output saved to {output_path}")
