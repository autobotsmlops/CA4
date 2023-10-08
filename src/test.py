import unittest
import json
from main import app, connect_to_db

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.db = connect_to_db()
        self.cursor = self.db.cursor()
        
        # Create a test database or use an existing one for testing
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS test_TODO")
        self.cursor.execute("USE test_TODO")
        # Perform any other necessary setup for your test database
    
    def tearDown(self):
        # Clean up the test database and close the database connection
        self.cursor.execute("DROP DATABASE IF EXISTS test_TODO")
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

    def test_get_tasks_route(self):
        response = self.app.get('/getTasks')
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['tasks']), 1)
    
    def test_update_task_route(self):
        data = {
            "description": "Updated Description",
            "status": "completed",
            "dueDate": "2023-11-15"
        }
        response = self.app.put('/updateTask/Task', data=json.dumps(data), content_type='application/json')
        print(response.json)
        self.assertEqual(response.status_code, 200)

    def test_search_task_route(self):
        response = self.app.get('/searchTask/Task')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_task_route(self):
        response = self.app.delete('/deleteTask/Task')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], True)
        

if __name__ == '__main__':
    unittest.main()
