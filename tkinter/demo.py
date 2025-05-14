from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.validation import Validator, ValidationError
import os

class PathValidator(Validator):
    def __init__(self, get_current_dir):
        self.get_current_dir = get_current_dir

    def validate(self, document):
        current_dir = self.get_current_dir()
        path = os.path.join(current_dir, document.text)
        if not os.path.exists(path):
            raise ValidationError(message="路径不存在")

class CLIFilePicker:
    def __init__(self):
        self.session = PromptSession()
        self.current_dir = os.getcwd()
        self.history = []

        # 传递获取当前目录的方法
        self.validator = PathValidator(lambda: self.current_dir)
    
    def _list_contents(self):
        """列出当前目录内容"""
        entries = []
        for item in os.listdir(self.current_dir):
            full_path = os.path.join(self.current_dir, item)
            entries.append({
                "name": f"[DIR] {item}" if os.path.isdir(full_path) else item,
                "path": full_path
            })
        return entries
    
    def _show_menu(self):
        """显示交互式菜单"""
        entries = self._list_contents()
        for i, entry in enumerate(entries, 1):
            print(f"{i:2}. {entry['name']}")
        print("\n0. 返回上级目录")
        print("00. 确认当前目录")
        print("---------------------------------")
    
    def pick_path(self):
        """主选择流程"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n当前目录: {self.current_dir}\n")
            self._show_menu()
            
            # 获取带自动补全的输入
            user_input = self.session.prompt(
                "请输入数字/路径 (支持Tab补全): ",
                completer=PathCompleter(only_directories=False),
                validator=self.validator,
                complete_while_typing=True
            )
            
            # 处理菜单选择
            if user_input.isdigit():
                choice = int(user_input)
                entries = self._list_contents()
                if 1 <= choice <= len(entries):
                    selected = entries[choice-1]["path"]
                    if os.path.isdir(selected):
                        self.current_dir = selected
                    else:
                        return selected
                elif choice == 0:
                    self.current_dir = os.path.dirname(self.current_dir)
                elif choice == 00:
                    return self.current_dir
            else:  # 处理直接路径输入
                path = os.path.abspath(
                    os.path.join(self.current_dir, user_input))
                if os.path.exists(path):
                    if os.path.isfile(path):
                        return path
                    else:
                        self.current_dir = path

if __name__ == "__main__":
    picker = CLIFilePicker()
    selected_path = picker.pick_path()
    print(f"\n已选择路径: {selected_path}")