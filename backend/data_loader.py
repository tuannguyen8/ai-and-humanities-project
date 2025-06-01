
from docx import Document
import json

def extract_categories(docx_path):
    doc = Document(docx_path)
    categories = []
    current = {}

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if text[0] in ["🎓", "🏠", "💰", "📅", "🩺", "🧾", "🚌", "📚", "🧑", "🌍"]:
            if current:
                categories.append(current)
                current = {}
            current["title"] = text[2:].strip()
        elif text.startswith("What Students Want:"):
            current["description"] = text.replace("What Students Want:", "").strip()
        elif text.startswith("Source:"):
            current["source"] = text.replace("Source:", "").strip()

    if current:
        categories.append(current)

    return {"PSU": categories}

def save_json(data, filename="data/university_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    extracted = extract_categories("data/Categories of Info.docx")
    save_json(extracted)
    print("✅ data extracted and saved.")
