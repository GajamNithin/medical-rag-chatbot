import re
import json

with open("medical_drugs.js", "r", encoding="utf-8") as f:
    text = f.read()

# remove variable declaration
text = re.sub(r'const\s+\w+\s*=\s*', '', text)

# remove comments
text = re.sub(r'//.*', '', text)

# add quotes around keys
text = re.sub(r'(\w+)\s*:', r'"\1":', text)

# remove trailing commas
text = re.sub(r',(\s*[}\]])', r'\1', text)

# remove semicolon
text = text.strip().rstrip(";")

# keep only array part
text = text[text.find("["):]

data = json.loads(text)

with open("medical_drugs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("JSON file successfully created")