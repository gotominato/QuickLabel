import json
import os
from pathlib import Path

class DataManager:
    def __init__(self, project_folder: Path, images: list):
        self.state_path = project_folder.joinpath('state.json')
        self.annotations_path = project_folder.joinpath('annotations.json')
        self.classes_path = project_folder.joinpath('classes.json')

        self._initialize_files()

    def _initialize_files(self) -> None:
        if not self.state_path.exists():
            with open(self.state_path, mode='w') as f:
                init_states = {'last_processed_index': -1}
                json.dump(init_states, f, indent=4)
        
        if not self.annotations_path.exists():
            with open(self.annotations_path, mode='w') as g:
                init_annotations = {'annotations': {}}
                json.dump(init_annotations, g, indent=4)

        if not self.classes_path.exists():
            with open(self.classes_path, mode='w') as h:
                init_classes = {'classes': []}
                json.dump(init_classes, h, indent=4)

    def load_states(self) -> dict:
        with open(self.state_path, mode='r') as f:
                states = json.load(f)
                
        return states
    
    def load_annotation(self) -> dict:
        with open(self.annotations_path, mode='r') as g:
                annotations = json.load(g)
                
        return annotations

    def load_classes(self) -> dict:
        with open(self.classes_path, mode='r') as h:
                classes = json.load(h)

        return classes

    def save_states(self, states: dict) -> None:
        with open(self.state_path, mode='w') as f:
            json.dump(states, f, indent=4)
    
    def save_annotation(self, annotations: dict) -> None:
        with open(self.annotations_path, mode='w', encoding='utf-8') as g:
            json.dump(annotations, g, indent=4, ensure_ascii=False)

    def save_class_list(self, class_list: dict) -> None:
        with open(self.classes_path, mode='w', encoding='utf-8') as h:
            json.dump(class_list, h, indent=4, ensure_ascii=False)