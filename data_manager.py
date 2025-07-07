import json
import os
from pathlib import Path

class DataManager:
    def __init__(self, project_folder: Path, images: list):
        self.state_path = project_folder.joinpath('state.json')
        self.annotations_path = project_folder.joinpath('annotations.json')
        self.labels_path = project_folder.joinpath('labels.json')
        
        self._initialize_files()
        
    def _initialize_files(self):
        if not self.state_path.exists():
            with open(self.state_path, mode='w') as f:
                init_states = {'last_processed_index': -1}
                json.dump(init_states, f, indent=4)
        
        if not self.annotations_path.exists():
            with open(self.annotations_path, mode='w') as g:
                init_annotations = {'annotations': {}}
                json.dump(init_annotations, g, indent=4)
        
        if not self.labels_path.exists():
            with open(self.labels_path, mode='w') as h:
                init_labels = {'labels': []}
                json.dump(init_labels, h, indent=4)
    
    def load_states(self) -> dict:
        with open(self.state_path, mode='r') as f:
                states = json.load(f)
                
        return states
    
    def load_annotation(self) -> dict:
        with open(self.annotations_path, mode='r') as g:
                annotations = json.load(g)
                
        return annotations
    
    def load_labels(self) -> dict:
        with open(self.labels_path, mode='r') as h:
                labels = json.load(h)
                
        return labels
    
    def update_sates(self, states: dict, number: int) -> dict:
        states['last_processed_index'] += number
            
        return states
    
    def update_annotation(self, annotations: dict, label: str, current_image: str) -> dict:
        return annotations['annotations'][current_image].append(label)
    
    def update_label_list(self, label_list: dict, add_label: str) -> dict:
        return label_list['labels'].append(add_label)