import unittest
import json
from main import app, connect_to_db

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.db = connect_to_db()
        self.cursor = self.db.cursor()
        self.taskID = None

        self.cursor.execute("DELETE FROM tasks")
        self.db.commit()

        
    def tearDown(self):
        # Clean up the test database and close the database connection
        self.cursor.close()
        self.db.close()
    
    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_add_task_route(self):
        data = {
            "name": "Task",
            "description": "Description for Task 1",
            "dueDate": "2023-10-31"
        }
        response = self.app.post('/addTask', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Retrieve the task ID from the response and store it for later use
        self.taskID = response.json['task']['id']

    def test_get_tasks_route(self):
        response = self.app.get('/getTasks')
        self.assertEqual(response.status_code, 200)
    
    def test_update_task_route(self):
        # Check if a task ID is available
        if self.taskID is not None:
            data = {
                "description": "Updated Description",
                "status": "completed",
                "dueDate": "2023-11-15"
            }
            response = self.app.put(f'/updateTask/{self.taskID}', data=json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_search_task_route(self):
        response = self.app.get('/searchTask/Task')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_task_route(self):
        # Check if a task ID is available
        if self.taskID is not None:
            response = self.app.delete(f'/deleteTask/{self.taskID}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], True)
        

if __name__ == '__main__':
    unittest.main()
