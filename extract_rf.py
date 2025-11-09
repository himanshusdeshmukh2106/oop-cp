import json

with open('Heart_disease_prediction/HeartDisease.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Extract code cells with RandomForest
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'RandomForest' in source or ('rf' in source.lower() and 'fit' in source):
            print(f"=== Cell {i} ===")
            print(source)
            print("\n")
