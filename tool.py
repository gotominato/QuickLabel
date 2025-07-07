import os
from pathlib import Path

from data_manager import DataManager
from terminal_view import TerminalView

class LabelingTool:
    def __init__(self, folder: str, mode: str):
        self.folder = Path(folder)
        self.mode = mode
        
        self.images = self._find_images()
        
        self.data_manager = DataManager(self.folder, self.images)
        self.terminal_view = TerminalView()
        
        self.states = self.data_manager.load_states()
        self.annotations = self.data_manager.load_annotation()
        self.label_list = self.data_manager.load_labels()
        
        self.current_index = -1
        self.current_image_name = None
        
    def _find_images(self) -> list:
        image_ext = ['*.jpg', '*.jpeg', '*.png']
        images = []
        for ext in image_ext:
            images.extend(self.folder.glob(ext))
            
        return sorted([str(i) for i in images])
    
    def run(self):
        if self.mode == 'single' or self.mode == 'multi':
            self._label_image()
        elif self.mode == 'add_label':
            self._add_label()
        else:
            self.terminal_view.show_message(f'エラー: モードが指定されていないか、不明なモード "{self.mode}" です。')
            raise NotImplementedError

    def _label_image(self):
        total_images = len(self.images)
        
        while True:
            self.current_index = self.states['last_processed_index'] + 1
            
            if self.current_index >= total_images:
                self.current_index = 0
            
            image_path = self.images[self.current_index]
            self.current_image = os.path.basename(image_path)
            
            labels = self.annotations['annotations'].get(self.current_image, [])
        
            display_data = {
                'mode': self.mode,
                'totla_images': total_images,
                'current_index': self.current_index,
                'label_list': self.label_list,
                'labels': labels,
                'image': self.current_image
            }
            
            self.terminal_view.render(display_data)
            
            command = self.terminal_view.get_input('> ')
            quit_flag = self._process_label_command(command)
            
            if quit_flag:
                break
        
    def _process_label_command(self, command: str) -> bool:
        command = command.replace(',', ' ')
        instruction = command.split()
        
        quit_flag = False
        
        if instruction[0].isdecimal():
            for label in instruction:
                self.annotations= self.data_manager.update_annotation(self.annotations, label, self.current_image)
        
        elif instruction[0].lower() == 'n':
            self.states = self.data_manager.update_sates(self.states, 1)
        
        elif instruction[0].lower() == 'p':
            self.states = self.data_manager.update_sates(self.states, -1)
        
        elif instruction[0].lower() == 's':
            pass
        
        elif instruction[0].lower() == 'a':
            if len(instruction) != 1:
                for add_label in instruction[1:]:
                    self.label_list = self.data_manager.update_label_list(self.label_list, add_label)
            else:
                self.terminal_view.show_message(f'エラー: ラベル名が入力されていません。')
        
        elif instruction[0].lower() == 'q':
            quit_flag = True
        
        else:
            self.terminal_view.show_message(f'エラー: コマンドが入力されていないか、不明なコマンド"{command}"です。')
            
        return quit_flag

    def _add_label(self):
        pass
    
