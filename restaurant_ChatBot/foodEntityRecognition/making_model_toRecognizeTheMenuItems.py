import re

# Path to your text file
file_path = 'r.txt'

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Regex pattern to match the names of the dishes
pattern = r'"name":\s*"[^"]*"'
names_list = []
# Find matches
matches = re.findall(pattern, content)

# Print the extracted names
for match in matches:
    names_list.append(match)

# Now, names_list contains all the extracted names
print(names_list)
import spacy
from spacy.tokens import Span
from spacy.tokens import DocBin
from spacy.util import filter_spans

# Load the spaCy model
nlp = spacy.blank("en")
doc_bin = DocBin()
elements = [
    "Cheese Burger Sandwich",
    "Shawarma Chicken Sandwich",
    "Shawarma Meat Sandwich",
    "Falafel Sandwich",
    "Crespi Chicken Sandwich",
    "Zinger Chicken Sandwich",
    "Pepperoni Pizza",
    "Mixed Pizza",
    "Hot Dog Pizza",
    "Four Seasons Pizza",
    "Hummus Plate",
    "French Fries Plate",
    "Vegetables Soup",
    "Strawberry Donut",
    "Vanilla Donut",
    "Chocolate Donut",
    "Chocolate Waffle",
    "Pan Cake",
    "Pepsi Can",
    "Pepsi Cup",
    "Pepsi Bottle",
    "Fresh Strawberry Juice"
]
label = "FOOD"
# Example text and label
for text in elements:
    doc = nlp.make_doc(text)
    span = doc.char_span(0, len(text), label=label, alignment_mode="contract")
    filtered_spans = filter_spans([span])
    doc.ents = filtered_spans
    doc_bin.add(doc)
doc_bin.to_disk("train.spacy")
