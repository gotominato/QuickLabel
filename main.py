import argparse

from tool import LabelingTool

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the labeling tool.")
    parser.add_argument('--folder', type=str, required=True, help='Path to the folder containing images.')
    args = parser.parse_args()
    
    folder = args.folder

    while True:
        mode = input("モードを選択してください (single, multi, add_class, exit): ").strip().lower()

        if mode in  ['single', 'multi', 'add_class']:
            tool = LabelingTool(folder=folder, mode=mode)
            tool.run()
        elif mode == 'exit':
            print("終了します。")
            break
        else:
            print("無効なモードです。再度入力してください。")
            continue