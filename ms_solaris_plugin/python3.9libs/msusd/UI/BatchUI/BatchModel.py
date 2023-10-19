from PySide2 import QtCore


class BatchModel(QtCore.QObject):
    taskChanged = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.taskChanged.emit()
