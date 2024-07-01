from PySide2 import QtWidgets, QtCore


class BatchView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.tasks_list = QtWidgets.QTableView()
        self.add_button = QtWidgets.QPushButton("Add Task")
        self.layout.addWidget(self.tasks_list)
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)

    def get_new_task(self):
        task, ok = QtWidgets.QInputDialog.getText(self, "New Task", "Enter a task:")
        return task if ok else None
