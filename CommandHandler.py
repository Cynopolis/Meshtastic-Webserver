class CommandHandler:
    def __init__(self, print_method):
        self.commands: dict = {}
        self.print = print_method
    
    def register_callback(self, key: str, callback):
        self.commands[key.lower()] = callback
        
    def parse_command(self, command : str):
        args :list[str] = command.split(" ")
        if args[0].lower() in self.commands:
            return_message = self.commands[args[0].lower()](args[1:])
            if not (return_message is None):
                self.print(return_message)
        else:
            self.print("Command not recognized. Type 'help' for a list of commands.")
        
        