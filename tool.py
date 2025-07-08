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
        
        self.message = ''
        self.quit_flag = False
        
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
            self.message = f'エラー: モードが指定されていないか、不明なモード "{self.mode}" です。'
            self.terminal_view.show_message(self.message)
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
            
            self.message = ''
            
            self.terminal_view.render(display_data, self.message)
            
            command = self.terminal_view.get_input('> ')
            self.quit_flag = self._process_label_command(command)

            if self.quit_flag:
                break
        
    def _process_label_command(self, command: str):
        command = command.replace(',', ' ')
        actions = command.split()
        
        if actions[0].isdecimal():
            for label in actions:
                self.annotations = self.data_manager.update_annotation(self.annotations, label, self.current_image)

        elif actions[0].lower() == 'n':
            self.states = self.data_manager.update_states(self.states, 1)

        elif actions[0].lower() == 'p':
            self.states = self.data_manager.update_states(self.states, -1)

        elif actions[0].lower() == 's':
            if len(actions) != 1:
                result = []
                result.extend(self.data_manager.search_label(self.label_list, actions[1:]))
                if not result:
                    self.message = f'エラー： 検索結果が見つかりません。'
                else:
                    self.message = f'検索結果: {" ".join(result)}'
            else:
                self.message = f'エラー: 検索するラベル名が入力されていません。'
        
        elif actions[0].lower() == 'a':
            if len(actions) != 1:
                self.label_list = self.data_manager.update_label_list(self.label_list, actions[1:])
                self.message = f'ラベル "{", ".join(actions[1:])}" を追加しました。'
            else:
                self.message = f'エラー: ラベル名が入力されていません。'
        
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
                'label_list': self.label_list.get('labels', []),
                'message': self.message
            }
            self.message = ''
            self.terminal_view.render(display_data, self.message)

            command = self.terminal_view.get_input("コマンド (d <ラベル名>:削除, q:終了) > ")

            self.quit_flag = self._process_add_label_command(command)

            if self.quit_flag:
                break

    def _process_add_label_command(self, command: str):
        """
        「ラベル追加モード」で入力されたコマンドを解釈し、状態を更新する。

        Returns:
            bool: ループを終了すべきならTrue、それ以外はFalse。
        """

        parts = command.split(' ', 1)
        action = parts[0].lower()

        if action == 'q':
            self.terminal_view.show_message("ラベルリストを保存して終了します。")
            self.quit_flag = True

        elif action == 'd':
            if len(parts) > 1:
                label_to_delete = parts[1]
                if label_to_delete in self.label_list['labels']:
                    self.label_list['labels'].remove(label_to_delete)
                    self.message = f"'{label_to_delete}' を削除しました。"
                else:
                    self.message = f"エラー: '{label_to_delete}' は存在しません。"
            else:
                self.message = "エラー: 削除するラベル名を指定してください。"

        else: # 追加処理
            new_label = command
            if new_label in self.label_list:
                self.message = f"エラー: '{new_label}' は既に存在します。"
            else:
                self.label_list['labels'].append(new_label)
                self.label_list['labels'].sort()
                self.message = f"'{new_label}' を追加しました。"
        
        self.data_manager.save_label_list(self.label_list)
    
