class Tasks:
    def __init__(self, id, name, description, dueDate, status=False):
        self.id = id
        self.name = name
        self.description = description
        self.status = status
        self.dueDate = dueDate

class Todo:
    def __init__(self, db):
        self.db = db

    def addTask(self, name, description, dueDate):
        cursor = self.db.cursor()
        status = False
        cursor.execute("INSERT INTO tasks (name, description, status, dueDate) VALUES (%s, %s, %s, %s)",
               (name, description, status, dueDate))

        self.db.commit()
        return Tasks(cursor.lastrowid, name, description, dueDate)

    def getTasks(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(Tasks(row[0], row[1], row[2], row[4], row[3]))
        return tasks

    def getTask(self, name):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE name=%s", (name,))
        row = cursor.fetchone()
        if row:
            return Tasks(row[0], row[1], row[2], row[4], row[3])
        return None

    def deleteTask(self, name):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tasks WHERE name=%s", (name,))
        self.db.commit()
        if cursor.rowcount > 0:
            return True
        return False

    def updateTask(self, name, description, status, dueDate):
        cursor = self.db.cursor()
        cursor.execute("UPDATE tasks SET description=%s, status=%s, dueDate=%s WHERE name=%s",
                       (description, status, dueDate, name))
        self.db.commit()
        if cursor.rowcount > 0:
            return self.getTask(name)
        return None

    def searchTask(self, name):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE name LIKE %s", ('%' + name + '%',))
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(Tasks(row[0], row[1], row[2], row[4], row[3]))
        return tasks
