import cv2
import os
from pathlib import Path
import readline

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
        
        self.message = ''
        self.quit_flag = False
        
        self.window_name = "QuickLabel Viewer"

    def _find_images(self) -> list:
        image_ext = ['*.jpg', '*.jpeg', '*.png']
        images = []
        for ext in image_ext:
            images.extend(self.folder.glob(ext))
            
        return sorted([str(i) for i in images])
    
    def run(self):
        if self.mode == 'single' or self.mode == 'multi':
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.window_name, 800, 600)
            self._label_image()
        elif self.mode == 'add_label':
            self._add_label()
        else:
            self.message = f'エラー: モードが指定されていないか、不明なモード "{self.mode}" です。'
            self.terminal_view.show_message(self.message)
            raise NotImplementedError

    def _label_image(self):
        total_images = len(self.images)
        while True:
            temp_index = self.current_index
            self.current_index = self.states['last_processed_index'] + 1
            
            if self.current_index >= total_images:
                self.current_index = 0
                self.states['last_processed_index'] = -1
            
            image_path = self.images[self.current_index]
            self.current_image = os.path.basename(image_path)
            
            labels = self.annotations['annotations'].get(self.current_image, [])
        
            display_data = {
                'mode': self.mode,
                'total_images': total_images,
                'current_index': self.current_index,
                'label_list': self.label_list['labels'],
                'labels': labels,
                'image': self.current_image
            }

            if self.current_index != temp_index:
                self._show_image(image_path)
            cv2.waitKey(1)
                
            self.terminal_view.render(display_data, self.message, self.mode)
            
            command = self.terminal_view.get_input('> ')
            self._process_label_command(command)

            if self.quit_flag:
                break
        
    def _process_label_command(self, command: str):
        command = command.replace(',', ' ')
        actions = command.split()
        
        if actions[0].isdecimal():
            if self.mode == 'single':
                if len(actions) != 1:
                    self.message = f'エラー: ラベル番号を一つだけ入力してください。'
                else:
                    if int(actions[0]) < 1 or int(actions[0]) > len(self.label_list['labels']):
                        self.message = f'エラー: ラベル番号は1から{len(self.label_list["labels"])}の範囲で入力してください。'
                    else:
                        self._update_annotation(actions[0], action='add')
            elif self.mode == 'multi':
                for label in actions:
                    if int(label) < 1 or int(label) > len(self.label_list['labels']):
                        self.message = f'エラー: ラベル番号は1から{len(self.label_list["labels"])}の範囲で入力してください。'
                    else:
                        self._update_annotation(label, action='add')

        elif actions[0].lower() == 'n':
            self._update_states(1)

        elif actions[0].lower() == 'p':
            self._update_states(-1)

        elif actions[0].lower() == 's':
            if len(actions) != 1:
                result = {}
                for s_label in actions[1:]:
                    result.update(self.data_manager.search_label(self.label_list, s_label))
                if not result:
                    self.message = f'エラー： 検索結果が見つかりません。'
                else:
                    self.message = f'検索結果: {" ".join([f"{k}: {v}" for k, v in result.items()])}'
            else:
                self.message = f'エラー: 検索するラベル名が入力されていません。'
        
        elif actions[0].lower() == 'a':
            if len(actions) != 1:
                for label in actions[1:]:
                    self._update_label_list(label, action='add')
                self.message = f'ラベル "{", ".join(actions[1:])}" を追加しました。'
            else:
                self.message = f'エラー: ラベル名が入力されていません。'
        
        elif actions[0].lower() == 'r':
            if len(actions) != 1:
                for label in actions[1:]:
                    self._update_annotation(label, action='remove')
            else:
                self.message = f'エラー: 削除するラベル名が入力されていません。'
        
        elif actions[0].lower() == 'q':
            self.quit_flag = True
            self.terminal_view.show_message("保存して終了します。")
        
        else:
            self.message = f'エラー: コマンドが入力されていないか、不明なコマンド"{command}"です。'
            
        self.data_manager.save_states(self.states)
        self.data_manager.save_annotation(self.annotations)
        self.data_manager.save_label_list(self.label_list)

    def _add_label(self):
        
        self.message = "追加したいラベル名を入力してください。"

        while True:
            display_data = {
                'mode': self.mode,
                'label_list': self.label_list['labels'],
                'message': self.message
            }
            self.message = ''
            self.terminal_view.render(display_data, self.message, self.mode)

            command = self.terminal_view.get_input('> ')

            self._process_add_label_command(command)

            if self.quit_flag:
                break

    def _process_add_label_command(self, command: str):
        command = command.replace(',', ' ')
        parts = command.split(' ', 1)
        action = parts[0].lower()

        if action == 'q':
            self.terminal_view.show_message("ラベルリストを保存して終了します。")
            self.quit_flag = True

        elif action == 'd':
            if len(parts) > 1:
                labels = parts[1: ]
                for label_to_delete in labels:
                    self._update_label_list(label_to_delete, action='remove')
                    self.message = f"'{label_to_delete}' を削除しました。"

            else:
                self.message = "エラー: 削除するラベル名を指定してください。"

        else:
            command = command.replace(',', ' ')
            new_label = command.split()
            if new_label in self.label_list['labels']:
                self.message = f"エラー: '{new_label}' は既に存在します。"
            else:
                for label in new_label:
                    self._update_label_list(label, action='add')
                new_label = ', '.join(new_label)
                self.message = f"'{new_label}' を追加しました。"
        
        self.data_manager.save_label_list(self.label_list)

    def _update_states(self, number: int) -> None:
        self.states['last_processed_index'] +=  number

    def _update_annotation(self, label: str, action: str) -> None:
        if self.current_image not in self.annotations['annotations']:
            self.annotations['annotations'][self.current_image] = []
            
        label_name = self.label_list['labels'][int(label) - 1]
        if action == "add":
            if label_name not in self.annotations['annotations'][self.current_image]:
                self.annotations['annotations'][self.current_image].append(label_name)

        elif action == "remove":
            if label_name in self.annotations['annotations'][self.current_image]:
                self.annotations['annotations'][self.current_image].remove(label_name)

    def _update_label_list(self, label: str, action: str) -> None:
        if action == "add":
            if label not in self.label_list['labels']:
                self.label_list['labels'].append(label)
        elif action == "remove":
            num_label = int(label)
            if 0 <= num_label - 1 < len(self.label_list['labels']):
                del self.label_list['labels'][num_label - 1]

    def _show_image(self, image_path: str) -> None:
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise FileNotFoundError
            cv2.imshow(self.window_name, img)
        except Exception as e:
            self.terminal_view.show_message(f"画像を表示できません: {e}")