import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import db, setup_db, Question, Category
from enum import unique
from uuid import uuid4


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format('postgres','245569','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_fetch_questions(self):
        """Test whether all questions are successfilly fetched"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        

    def test_fetch_categories(self):
        """Test whether all categories are successfilly fetched"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        
        
    def test_200_valid_page_request(self):
        """Test if user enters a valid page number"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        
        
    def test_404_invalid_page_request(self):
        """Test if user enters an invalid page number"""
        res = self.client().get('/questions?page=500')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'Not found.')
        
        
    def test_create_question(self):
        """Test successful creation of a new question"""
        #get id from uuid
        unique_id = str(uuid4())
        new_ques = {
            'question': 'Question: ' + unique_id,
            'answer': 'Answer: ' + unique_id,
            'difficulty': 1,
            'category': 1
        }

        #send request to create new question
        res = self.client().post('/questions', json=new_ques)
        data = json.loads(res.data)

        #check if the question is created successfully.
        ques = Question.query.filter_by(question='Question: '+unique_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(ques.answer,"Answer: "+unique_id)

        
    def test_delete_question(self):
        """ Test successful question deletion. """
        # generate question for test case
        ques = Question(question="Can I delete this?",answer='ok', category=1, difficulty=1)
        ques.insert()
        id = ques.id

        res = self.client().delete('/questions/'+str(id))
        data = json.loads(res.data)

        ques = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertEqual(ques, None)
        
        
    def test_422_create_question(self):
            """test question creation failure"""
            
            existing_ques = Question.query.all()

            #send nothing
            res = self.client().post('/questions', json={})
            data = json.loads(res.data)

            updated_ques = Question.query.all()

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertTrue(len(existing_ques) == len(updated_ques))'''


    def test_search_question(self):
            """test successful retireval of search term"""
            
            res = self.client().post('/questions/search', json={
                'searchTerm': 'What'})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['questions']) > 0)
            self.assertIsNotNone(data['questions'])
            self.assertIsNotNone(data['total_questions'])
            print('passed',res.status_code)
        

    '''def test_404_search_questions(self):
            """test 404 - search not found"""
            res = self.client().post('/questions/search', json={'searchTerm': ''})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], "Not found.")


    def test_fetch_category_questions(self):
            """test successful retrieval of questions by categories"""

            res = self.client().get('/categories/1/questions')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['questions']))
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['current_category'])
            
            
    def test_404_fetch_category_questions(self):
            """test 404 - no question from category"""
            res = self.client().get('/categories/123456/questions')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "Not found.")
            
            
    def test_fetch_quiz(self):
            """test successful quiz"""

            #choose a category
            category = Category.query.all()[2]

            quiz = {'previous_questions': [], 'quiz_category': {
                'type': category.type, 'id': category.id}}

            res = self.client().post('/quizzes', json=quiz)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            

    def test_422_fetch_quiz(self):
            """test 422 - failed quiz round"""
            res = self.client().post('/quizzes', json={})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable request')'''

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()