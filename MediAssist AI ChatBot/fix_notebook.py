import json
import sys

def fix_notebook(notebook_path):
    """Fix notebook by removing widgets without 'state' key or adding empty state"""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Check if widgets exist in metadata
    if 'metadata' in nb and 'widgets' in nb['metadata']:
        widgets = nb['metadata']['widgets']
        
        # Check if it's the widget-state format
        if 'application/vnd.jupyter.widget-state+json' in widgets:
            widget_state = widgets['application/vnd.jupyter.widget-state+json']
            fixed_widgets = {}
            
            # Only keep widgets that have a 'state' key
            for widget_id, widget_data in widget_state.items():
                if isinstance(widget_data, dict) and 'state' in widget_data:
                    fixed_widgets[widget_id] = widget_data
                # If widget doesn't have state but has other required fields, add empty state
                elif isinstance(widget_data, dict) and 'model_module' in widget_data:
                    widget_data['state'] = {}
                    fixed_widgets[widget_id] = widget_data
            
            # Update the widgets
            widgets['application/vnd.jupyter.widget-state+json'] = fixed_widgets
    
    # Write back the fixed notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print(f"Fixed notebook: {notebook_path}")

if __name__ == '__main__':
    notebook_path = 'MediAssist AI ChatBot/Models/Fine tune & Evaluation/Fine_tuned_MedAlpaca.ipynb'
    fix_notebook(notebook_path)

