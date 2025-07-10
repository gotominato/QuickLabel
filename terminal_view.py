import os
import readline

class TerminalView:
    def __init__(self):
        pass
    
    def render(self, display_data: dict, message: str, mode: str = 'N/A'):
        os.system('cls' if os.name == 'nt' else 'clear')
        if mode == 'single' or mode == 'multi':
            self.view_label_image(display_data, message)
        elif mode == 'add_label':
            self.view_add_label(display_data, message)
        
    def view_label_image(self, display_data: dict, message: str):
        mode = display_data.get('mode', 'N/A')
        total_images = display_data.get('total_images', 0)
        current_index = display_data.get('current_index', -1)
        label_list = display_data.get('label_list', [])
        current_labels = display_data.get('labels', [])
        image_name = display_data.get('image', 'N/A')

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

        if message != '':
            self.show_message(f"[INFO] {message}")
            print("----------------------------------------------")
            
    def view_add_label(self, display_data: dict, message: str):
        mode = display_data.get('mode', 'N/A')
        label_list = display_data.get('label_list', [])
        
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

        if message != '':
            self.show_message(f"[INFO] {message}")
            print("----------------------------------------------")

    def get_input(self, input_sentence):
        command = input(input_sentence)
        
        return command
    
    def show_message(self, message):
        print(message)