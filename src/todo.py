class Tasks:
    def __init__(self, id, name, description, dueDate, status=False):
        self.id = id
        self.name = name
        self.description = description
        self.status = status
        self.dueDate = dueDate


class Todo:
    def __init__(self):
        self.index = 0
        self.tasks = []

    def addTask(self, name, description, dueDate):
        self.index = self.index + 1
        task = Tasks(self.index, name, description, dueDate)
        self.tasks.append(task)
        return task

    def getTasks(self):
        return self.tasks
    
    def getTask(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        return None
    
    def deleteTask(self, name):
        task = self.getTask(name)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def updateTask(self, name, description, status, dueDate):
        task = self.getTask(name)
        if task:
            task.description = description
            task.status = status
            task.dueDate = dueDate
            return task
        return None
    
    def searchTask(self, name):
        tasks = []
        for task in self.tasks:
            if name in task.name:
                tasks.append(task)
        return tasks
    
