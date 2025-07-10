import argparse

from tool import LabelingTool

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the labeling tool.")
    parser.add_argument('--folder', type=str, required=True, help='Path to the folder containing images.')
    parser.add_argument('--mode', type=str, required=True, default=None, choices=['single', 'multi', 'add_label'], help='Mode of operation: single, multi, or add_label.')
    args = parser.parse_args()
    
    folder = args.folder
    mode = args.mode

    tool = LabelingTool(folder=folder, mode=mode)
    tool.run()