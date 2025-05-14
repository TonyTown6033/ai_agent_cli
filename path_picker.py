from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator, ValidationError
import os

class PathValidator(Validator):
    def __init__(self, get_current_dir):
        self.get_current_dir = get_current_dir

    def validate(self, document):
        # 允许空输入（直接回车）
        if document.text.strip() == "":
            return
        current_dir = self.get_current_dir()
        path = os.path.abspath(os.path.join(current_dir, document.text))
        if not os.path.exists(os.path.dirname(path)) and not os.path.exists(path):
            raise ValidationError(message="路径不存在")

class SmartPathCompleter(Completer):
    def __init__(self, get_current_dir):
        self.get_current_dir = get_current_dir

    def get_completions(self, document, complete_event):
        text = document.text
        current_dir = self.get_current_dir()
        # 判断是否以../开头
        if text.startswith("../"):
            base_dir = os.path.abspath(os.path.join(current_dir, text))
        else:
            base_dir = os.path.abspath(os.path.join(current_dir, os.path.dirname(text)))
        if os.path.isdir(base_dir):
            for item in os.listdir(base_dir):
                yield Completion(
                    os.path.join(os.path.dirname(text), item) if text else item,
                    start_position=-len(text)
                )

class CLIFilePicker:
    def __init__(self):
        self.session = PromptSession()
        self.current_dir = os.getcwd()
        self.history = []
        self.validator = PathValidator(lambda: self.current_dir)
        self.completer = SmartPathCompleter(lambda: self.current_dir)
    
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
        print("\n../  返回上级目录（可多级）")
        print(".   确认当前目录")
        print("---------------------------------")
    
    def pick_path(self):
        """主选择流程"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n当前目录: {self.current_dir}\n")
            self._show_menu()
            
            # 获取带自动补全的输入
            user_input = self.session.prompt(
                "请输入数字/路径/../（上级）/ .（当前）: ",
                completer=self.completer,
                validator=self.validator,
                complete_while_typing=True
            )
            
            # 空输入等价于当前目录
            if user_input.strip() == "" or user_input == ".":
                return self.current_dir
            elif user_input.isdigit():
                choice = int(user_input)
                entries = self._list_contents()
                if 1 <= choice <= len(entries):
                    selected = entries[choice-1]["path"]
                    if os.path.isdir(selected):
                        self.current_dir = selected
                    else:
                        return selected
            else:
                # 支持 ../ 多级返回和路径补全
                path = os.path.abspath(os.path.join(self.current_dir, user_input))
                if os.path.exists(path):
                    # 不管是文件还是目录都直接返回
                    return path

if __name__ == "__main__":
    picker = CLIFilePicker()
    selected_path = picker.pick_path()
    print(f"\n已选择路径: {selected_path}")