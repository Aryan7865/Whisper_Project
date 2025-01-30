import spacy
import re

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Read the full transcription from the file
with open("full_transcription.txt", "r") as f:
    full_transcription = f.read()

# Process the full transcription
doc = nlp(full_transcription)

# Define keywords to identify sections
keywords = {
    "complaints": ["issue", "symptom", "problem", "feeling", "concern", "experiencing", "trouble", "swelling", "pain"],
    "diagnosis": ["diagnosis", "condition", "find", "result", "examination", "determine", "look like", "seem"],
    "notes": ["note", "remind", "remember", "mention", "appointment", "reading", "instruction", "advice"],
    "follow_up": ["follow-up", "next appointment", "review", "progress", "check", "see you"],
    "drugs": ["medicine", "medication", "drug", "prescribe", "tablet", "pill", "capsule"],
    "illness_related_to_diabetes": ["diabetes", "sugar levels", "blood sugar", "diabetic", "monitoring"]
}

# Extract information based on keywords
sections = {key: [] for key in keywords}

for sentence in doc.sents:
    for key, words in keywords.items():
        if any(word in sentence.text.lower() for word in words):
            sections[key].append(sentence.text)

# Combine the extracted sections into a report with bullet points
report = {key: "\n".join(f"- {sentence}" for sentence in sentences) for key, sentences in sections.items()}

# Save the report to a text file
with open("report.txt", "w") as f:
    for key, text in report.items():
        f.write(f"{key.capitalize()}:\n{text}\n\n")

# Generate an HTML file
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        h2 {
            border-bottom: 2px solid #333;
            padding-bottom: 5px;
            margin-bottom: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        ul li {
            margin: 5px 0;
        }
        @media (max-width: 768px) {
            body {
                margin: 10px;
                padding: 10px;
            }
            h2 {
                font-size: 1.5em;
            }
        }
        @media (max-width: 480px) {
            h2 {
                font-size: 1.2em;
            }
        }
    </style>
</head>
<body>
"""

# Append sections to the HTML content
for key, text in report.items():
    html_content += f"<h2>{key.capitalize()}</h2><ul>"
    for line in text.split("\n"):
        if line:
            html_content += f"<li>{line[2:]}</li>"
    html_content += "</ul>"

# Extract drug information using more flexible patterns
drug_pattern = re.compile(r'\b(\w+)\s*(?:\d+ mg)?\s*(?:dosage would be|take|apply|every|before|after)?', re.IGNORECASE)
dosage_pattern = re.compile(r'\b\d+ mg\b', re.IGNORECASE)
timing_pattern = re.compile(r'(twice a day|three times a day|every eight hours|daily|once a day|morning|evening|night)', re.IGNORECASE)
instructions_pattern = re.compile(r'(before breakfast and dinner|after cleaning the ulcer|for \d+ days|every \d+ hours|as directed)', re.IGNORECASE)

drugs = []
for sentence in doc.sents:
    drug_matches = drug_pattern.findall(sentence.text)
    for drug in drug_matches:
        if drug:
            dosage_match = dosage_pattern.search(sentence.text)
            timing_match = timing_pattern.search(sentence.text)
            instructions_match = instructions_pattern.search(sentence.text)

            dosage = dosage_match.group() if dosage_match else 'N/A'
            timing = timing_match.group() if timing_match else 'N/A'
            instructions = instructions_match.group() if instructions_match else 'N/A'

            drugs.append((drug.strip(), dosage, timing, instructions))

# Add the drugs section to the HTML content
html_content += "<h2>Drugs</h2>"
if drugs:
    html_content += "<ul>"
    for drug, dosage, timing, instructions in drugs:
        drug_info = f"{drug.capitalize()} - Dosage: {dosage}, Timing: {timing}, Instructions: {instructions}"
        html_content += f"<li>{drug_info}</li>"
    html_content += "</ul>"
else:
    html_content += "<p>No drugs prescribed.</p>"

# Close the HTML content
html_content += """
</body>
</html>
"""

# Save the HTML content to a file
with open("report.html", "w") as f:
    f.write(html_content)

print("Report generation completed.")
