import json
import os

class DataManager:
    def __init__(self, project_folder:str):
        self.state_path = f"{project_folder}/state.json"
        self.annotations_path = f"{project_folder}/annotations.json"
        self.labels_path = f"{project_folder}/labels.json"
        
        self._initialize_files()
        
    def _initialize_files(self):
        if not os.path.exists(self.state_path):
            with open(self.state_path, mode='w') as f:
                init_states = {"last_processed_index": -1, "jump_origin_index": 'null'}
                json.dump(init_states, f, indent=4)
        
        if not os.path.exists(self.annotations_path):
            with open(self.annotations_path, mode='w') as g:
                init_annotations = {'annotations': []}
                json.dump(init_annotations, g, indent=4)
        
        if not os.path.exists(self.labels_path):
            with open(self.labels_path, mode='w') as h:
                init_labels = {'label': []}
                json.dump(init_labels, h, indent=4)
    
    def load_states(self):
        with open(self.state_path, mode='r') as f:
                states = json.load(f)
                
        return states
    
    def load_annotation(self):
        with open(self.annotations_path, mode='r') as g:
                annotations = json.load(g)
                
        return annotations
    
    def load_labels(self):
        with open(self.labels_path, mode='r') as h:
                labels = json.load(h)
                
        return labels