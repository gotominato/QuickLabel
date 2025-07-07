class TerminalView:
    def __init__(self):
        pass
    
    def render(self, display_data: dict):
        pass
    
    def get_input(self, input_sentence):
        command = input(input_sentence)
        
        return command
    
    def show_message(self, message):
        print(message)