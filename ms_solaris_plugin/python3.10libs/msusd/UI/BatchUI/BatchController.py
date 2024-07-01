from PySide2.QtCore import Slot


class BatchController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.add_button.clicked.connect(self.add_task)
        self.model.taskChanged.connect(self.update_view)

    def add_task(self):
        print("new_task")
        new_task = self.view.get_new_task()
        if new_task:
            self.model.add_task(new_task)

    def update_view(self):
        tasks = self.model.tasks
        self.view.tasks_list.clear()
        self.view.tasks_list.addItems(tasks)
