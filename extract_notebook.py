import json

with open('Heart_disease_prediction/HeartDisease.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f"Total cells: {len(notebook['cells'])}\n")

# Extract code cells with model training
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if any(keyword in source for keyword in ['fit(', 'RandomForest', 'DecisionTree', 'KNeighbors', 'GaussianNB', 'accuracy_score']):
            print(f"=== Cell {i} ===")
            print(source)
            print("\n")
