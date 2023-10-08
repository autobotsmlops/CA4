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
        cursor = self.db.cursor(buffered=True)
        status = False
        cursor.execute("INSERT INTO tasks (name, description, status, dueDate) VALUES (%s, %s, %s, %s)",
               (name, description, status, dueDate))

        self.db.commit()
        return Tasks(cursor.lastrowid, name, description, dueDate)

    def getTasks(self):
        cursor = self.db.cursor(buffered=True)
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(Tasks(row[0], row[1], row[2], row[4], row[3]))
        return tasks

    def getTask(self, name):
        cursor = self.db.cursor(buffered=True)
        cursor.execute("SELECT * FROM tasks WHERE name=%s", (name,))
        row = cursor.fetchone()
        if row:
            return Tasks(row[0], row[1], row[2], row[4], row[3])
        return None

    def deleteTask(self, id):
        cursor = self.db.cursor(buffered=True)
        cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
        self.db.commit()
        if cursor.rowcount > 0:
            return True
        return False

    def updateTask(self, id, name, description, status, dueDate):
        cursor = self.db.cursor(buffered=True)
        cursor.execute("UPDATE tasks SET name=%s, description=%s, status=%s, dueDate=%s WHERE id=%s",
                       (name, description, status, dueDate, id))
        self.db.commit()
        return self.getTask(name)

    def searchTask(self, name):
        cursor = self.db.cursor(buffered=True)
        cursor.execute("SELECT * FROM tasks WHERE name LIKE %s", ('%' + name + '%',))
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append(Tasks(row[0], row[1], row[2], row[4], row[3]))
        return tasks
