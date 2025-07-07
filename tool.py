import os

from data_manager import DataManager

class LabelingTool:
    def __init__(self, folder: str, mode: str):
        self.folder = folder
        self.mode = mode
        
        self.data_manager = DataManager(self.folder)
        
        self.states = self.data_manager.load_states()
        self.annotations = self.data_manager.load_annotation()
        self.labels = self.data_manager.load_labels()

    def run(self):
        if self.mode == 'single' or self.mode == 'multi':
            self.label_image()
        elif self.mode == 'add_label':
            self.add_label()
        else:
            raise NotImplementedError

    def label_image(self):
        pass

    def add_label(self):
        pass
