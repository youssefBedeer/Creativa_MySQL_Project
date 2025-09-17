from commands.add_commands import AddRowCommand,DeleteRowCommand,ShowTableCommand,GetTableColumns

class CommandFactory:
    
    def create_command(command_name: str, *args, **kwargs):
        __commands = {
            "add_row" : AddRowCommand,
            "delete_row" : DeleteRowCommand,
            "show_table": ShowTableCommand,
            "show_columns":GetTableColumns
        }
        return __commands[command_name](*args, **kwargs) if command_name in __commands \
            else print(f"command '{command_name}' NOT in available commands --> {list(__commands.keys())}")