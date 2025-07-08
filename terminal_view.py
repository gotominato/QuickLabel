import os

class TerminalView:
    def __init__(self):
        pass
    
    def render(self, display_data: dict, message: str):
        os.system('cls' if os.name == 'nt' else 'clear')

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
            print(f"[INFO] {message}")
            print("----------------------------------------------")

    def get_input(self, input_sentence):
        command = input(input_sentence)
        
        return command
    
    def show_message(self, message):
        print(message)