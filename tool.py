import cv2
import os
from pathlib import Path
import readline

from data_manager import DataManager
from terminal_view import TerminalView

class LabelingTool:
    def __init__(self, folder: str, mode: str) -> None:
        self.folder = Path(folder)
        self.mode = mode
        
        self.images = self._find_images()
        
        self.data_manager = DataManager(self.folder, self.images)
        self.terminal_view = TerminalView()
        
        self.states = self.data_manager.load_states()
        self.annotations = self.data_manager.load_annotation()
        self.classes_list = self.data_manager.load_classes()

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

    def run(self) -> None:
        if self.mode == 'single' or self.mode == 'multi':
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.window_name, 800, 600)
            self._label_image()
        elif self.mode == 'add_class':
            self._add_class()
        else:
            self.message = f'エラー: モードが指定されていないか、不明なモード "{self.mode}" です。'
            self.terminal_view.show_message(self.message)
            raise NotImplementedError

    def _label_image(self) -> None:
        total_images = len(self.images)
        while True:
            temp_index = self.current_index
            self.current_index = self.states['last_processed_index'] + 1
            
            if self.current_index >= total_images:
                self.current_index = 0
                self.states['last_processed_index'] = -1
            
            image_path = self.images[self.current_index]
            self.current_image = os.path.basename(image_path)
        
            display_data = {
                'mode': self.mode,
                'total_images': total_images,
                'current_index': self.current_index,
                'class_list': self.classes_list['classes'],
                'labels': self.annotations['annotations'].get(self.current_image, []),
                'image': self.current_image,
                'message': self.message
            }
            
            self.terminal_view.render(display_data, self.mode)
            
            self.message = ''

            if self.current_index != temp_index:
                self._show_image(image_path)
            cv2.waitKey(1)

            command = self.terminal_view.get_input('> ')
            self._process_label_command(command)

            if self.quit_flag:
                break

    def _process_label_command(self, command: str) -> None:
        command = command.replace(',', ' ')
        parts = command.split()
        action = parts[0].lower()

        if action.isdecimal():
            if self.mode == 'single':
                if len(self.annotations['annotations'].get(self.current_image, [])) > 0:
                    self.message = f'エラー: 既にラベルが付けられています。'
                else:
                    if len(parts) != 1:
                        self.message = f'エラー: クラス番号を一つだけ入力してください。'
                    else:
                        if int(action) < 1 or int(action) > len(self.classes_list['classes']):
                            self.message = f'エラー: クラス番号は1から{len(self.classes_list["classes"])}の範囲で入力してください。'
                        else:
                            self._update_annotation(action, action='add')
                            self.message = f'クラス "{self.classes_list["classes"][int(action) - 1]}" を追加しました。'

            elif self.mode == 'multi':
                for class_id in parts:
                    if int(class_id) < 1 or int(class_id) > len(self.classes_list['classes']):
                        self.message = f'エラー: クラス番号は1から{len(self.classes_list["classes"])}の範囲で入力してください。'
                    else:
                        self._update_annotation(class_id, action='add')
                self.message = f'クラス "{", ".join([self.classes_list["classes"][int(c) - 1] for c in parts])}" を追加しました。'

        elif action == 'n':
            self._update_states(1)

        elif action == 'p':
            self._update_states(-1)

        elif action == 's':
            if len(parts) != 1:
                result = {}
                for s_class in parts[1:]:
                    result.update(self._search_class(s_class))

                if not result:
                    self.message = f'エラー： 検索結果が見つかりません。'
                else:
                    self.message = f'検索結果: {" ".join([f"{k}: {v}" for k, v in result.items()])}'      
            else:
                self.message = f'エラー: 検索するクラス名が入力されていません。'

        elif action == 'a':
            if len(parts) != 1:
                for class_name in parts[1:]:
                    self._update_class_list(class_name, action='add')
                self.message = f'クラス "{", ".join(parts[1:])}" を追加しました。'
            else:
                self.message = f'エラー: クラス名が入力されていません。'

        elif action == 'r':
            if len(parts) != 1:
                del_labels = []
                labels = list(map(int, parts[1:]))
                labels.sort()
                labels.reverse()
                labels = list(map(str, labels))
                for label in labels:
                    if len(self.classes_list['classes']) < int(label)-1 or int(label) < 1:
                        self.message = f'エラー: 削除するクラス番号は1から{len(self.classes_list["classes"])}の範囲で入力してください。'
                    else:
                        del_labels.append(self.classes_list['classes'][int(label) - 1])
                        self._update_annotation(label, action='remove')
                self.message = f'クラス "{", ".join(del_labels)}" を削除しました。'
            else:
                self.message = f'エラー: 削除するラベル名が入力されていません。'

        elif action == 'q':
            self.quit_flag = True
            self.terminal_view.show_message('保存して終了します。')

        else:
            self.message = f'エラー: コマンドが入力されていないか、不明なコマンド"{command}"です。'
            
        self.data_manager.save_states(self.states)
        self.data_manager.save_annotation(self.annotations)
        self.data_manager.save_class_list(self.classes_list)

    def _add_class(self) -> None:

        self.message = '追加したいクラス名を入力してください。'

        while True:
            display_data = {
                'mode': self.mode,
                'class_list': self.classes_list['classes'],
                'message': self.message
            }
            self.message = ''
            self.terminal_view.render(display_data, self.mode)

            command = self.terminal_view.get_input('> ')

            self._process_add_class_command(command)

            if self.quit_flag:
                break

    def _process_add_class_command(self, command: str) -> None:
        command = command.replace(',', ' ')
        parts = command.split(' ')
        action = parts[0].lower()

        if action == 'q':
            self.terminal_view.show_message('クラスリストを保存して終了します。')
            self.quit_flag = True

        elif action == 'd':
            if len(parts) > 1:
                del_classes = []
                classes = list(map(int, parts[1:]))
                classes.sort()
                classes.reverse()
                classes = list(map(str, classes))
                for class_to_delete in classes:
                    if len(self.classes_list['classes']) < int(class_to_delete)-1 or int(class_to_delete) < 1:
                        self.message = f'エラー: 削除するクラス番号は1から{len(self.classes_list["classes"])}の範囲で入力してください。'
                    else:
                        del_classes.append(self.classes_list['classes'][int(class_to_delete) - 1])
                        self._update_class_list(class_to_delete, action='remove')
                self.message = f'クラス "{", ".join(del_classes)}" を削除しました。'

            else:
                self.message = 'エラー: 削除するクラス名を指定してください。'

        else:
            command = command.replace(',', ' ')
            new_class = command.split()
            if new_class in self.classes_list['classes']:
                self.message = f'エラー: "{new_class}" は既に存在します。'
            else:
                for class_to_add in new_class:
                    self._update_class_list(class_to_add, action='add')
                new_class = ', '.join(new_class)
                self.message = f'クラス "{new_class}" を追加しました。'

        self.data_manager.save_class_list(self.classes_list)

    def _update_states(self, number: int) -> None:
        self.states['last_processed_index'] +=  number

    def _update_annotation(self, label: str, action: str) -> None:
        if self.current_image not in self.annotations['annotations']:
            self.annotations['annotations'][self.current_image] = []

        class_name = self.classes_list['classes'][int(label) - 1]
        if action == "add":
            if class_name not in self.annotations['annotations'][self.current_image]:
                self.annotations['annotations'][self.current_image].append(class_name)

        elif action == "remove":
            if class_name in self.annotations['annotations'][self.current_image]:
                self.annotations['annotations'][self.current_image].remove(class_name)

    def _update_class_list(self, class_name: str, action: str) -> None:
        if action == "add":
            if class_name not in self.classes_list['classes']:
                self.classes_list['classes'].append(class_name)
        elif action == "remove":
            num_class = int(class_name)
            if 0 <= num_class - 1 < len(self.classes_list['classes']):
                del self.classes_list['classes'][num_class - 1]

    def _show_image(self, image_path: str) -> None:
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise FileNotFoundError
            cv2.imshow(self.window_name, img)
        except Exception as e:
            self.terminal_view.show_message(f'画像を表示できません: {e}')

    def _search_class(self, search_classes: str) -> dict:
        result = {}
        for class_name in self.classes_list['classes']:
            if search_classes in class_name:
                class_index = self.classes_list['classes'].index(class_name)
                result[class_index+1] = class_name
        return result