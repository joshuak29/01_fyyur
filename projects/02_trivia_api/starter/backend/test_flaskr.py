import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_question = {'question':"What's this?", 'answer':'Nothing', 'category':6, 'difficulty':3}
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        body = json.loads(res.data) 
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(body['categories']))
    
    def test_get_questions_paginated(self):
        res = self.client().get('/questions')
        body = json.loads(res.data) 
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(body['questions']))
        self.assertTrue(body['totalQuestions'])
        self.assertTrue(len(body['categories']))
    
    def test_400_invalid_page(self):
        res = self.client().get('/questions?page=100')
        body = json.loads(res.data) 
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(body['error'], 400)
        self.assertEqual(body['message'], 'bad request')
        
    def test_delete_question(self):
        res = self.client().delete('/questions/32')
        body = json.loads(res.data) 
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body['deleted'], 12)
    
    def test_404_fail_delete_invalid_question(self):
        res = self.client().delete('/questions/100')
        body = json.loads(res.data) 
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'resource not found')
        
    
        
    def test_get_query_by_category(self):
        res = self.client().get('/categories/2/questions')
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(body['questions']))
        self.assertTrue(body['totalQuestions'])
        self.assertTrue(body['currentCategory'], 'Art')   
    
    def test_failed_get_query_by_category(self):      
        res = self.client().get('/categories/10/questions')
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'resource not found')
        
    def test_post_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(body['questions']))
        self.assertTrue(body['totalQuestions'])
        
    def test_post_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        
    def test_failed_search_question(self):
        res = self.client().post('/questions')
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(body['error'], 405)
        self.assertEqual(body['message'], 'method not allowed')
        
    
    def test_get_quizzes(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category':'Art'})
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(body))
    
    def test_failed_get_quizzes(self):
        res = self.client().post('/quizzes', json={'previou':'new'})
        body = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()