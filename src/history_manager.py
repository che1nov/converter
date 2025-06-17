import json
import os


class HistoryManager:
    def __init__(self, file_path=None):
        if file_path is None:
            project_root = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            file_path = os.path.join(project_root, "data", "operations.json")
        self.file_path = file_path
        self.operations = self.load_operations()

    def load_operations(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("⚠️ Corrupted history file. Resetting...")
                return []
        with open(self.file_path, "w") as file:
            json.dump([], file)
        return []

    def save_operations(self):
        with open(self.file_path, "w") as file:
            json.dump(self.operations, file, indent=4)

    def add_operation(self, operation):
        if operation not in self.operations:
            self.operations.append(operation)
        self.save_operations()

    def get_operations(self):
        return self.operations
