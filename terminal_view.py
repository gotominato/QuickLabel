import os
import readline

class TerminalView:
    def __init__(self):
        pass
    
    def render(self, display_data: dict, mode: str = 'N/A') -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        if mode == 'single' or mode == 'multi':
            self.view_label_image(display_data)
        elif mode == 'add_label':
            self.view_add_label(display_data)
        
    def view_label_image(self, display_data: dict) -> None:
        mode = display_data.get('mode', 'N/A')
        total_images = display_data.get('total_images', 0)
        current_index = display_data.get('current_index', -1)
        label_list = display_data.get('label_list', [])
        current_labels = display_data.get('labels', [])
        image_name = display_data.get('image', 'N/A')
        message = display_data.get('message', '')

        print("==================================================")
        print(f" QuickLabel | モード: {mode}")
        print("==================================================")
        print(f"画像: {current_index + 1} / {total_images}")
        print(f"ファイル名: {image_name}")
        print("--------------------------------------------------")

        if current_labels:
            print(f"[現在のラベル: {', '.join(current_labels)}]")
        else:
            print("[現在のラベル: (まだありません)]")
        print("--------------------------------------------------")

        print("利用可能なラベル:")

        for i, label in enumerate(label_list, 1):
            print(f"{i:>3}: {label:<20}", end="")
            if i % 3 == 0:
                print()
        print("\n----------------------------------------------")

        print('コマンド: (＜ラベル番号＞:ラベル追加, n: 次へ, p: 前へ, s ＜キーワード＞: 検索, a ＜ラベル名＞: 追加, r ＜ラベル番号＞: 削除, q: 終了)')
        print("----------------------------------------------")

        if message != '':
            self.show_message(f"[INFO] {message}")
            print("----------------------------------------------")
            
    def view_add_label(self, display_data: dict) -> None:
        mode = display_data.get('mode', 'N/A')
        label_list = display_data.get('label_list', [])
        message = display_data.get('message', '')

        print("==================================================")
        print(f" QuickLabel | モード: {mode}")
        print("==================================================")
        
        if label_list:
            print("現在のラベル:")
            for i, label in enumerate(label_list, 1):
                print(f"{i:>3}: {label:<20}", end="")
                if i % 3 == 0:
                    print()
            print("\n----------------------------------------------")
        else:
            print("[現在のラベル: (まだありません)]")
            print("----------------------------------------------")
        
        print('コマンド: (＜ラベル名＞: 追加, d ＜ラベル番号＞: 削除, q: 終了)')
        print("----------------------------------------------")

        if message != '':
            self.show_message(f"[INFO] {message}")
            print("----------------------------------------------")

    def get_input(self, input_sentence) -> str:
        command = input(input_sentence)
        
        return command

    def show_message(self, message) -> None:
        print(message)