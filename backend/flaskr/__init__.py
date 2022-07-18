import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Helpers
def paginate(request, data):
    page = request.args.get('page',1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = page * QUESTIONS_PER_PAGE
    questions = [i.format() for i in data]
    response = questions[start:end]
    return response

def format_categories(categories):
    response = {}
    for category in categories:
        response[category.id] = category.type
    return response



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Autorization,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,PATCH,POST,DELETE,OPTIONS')

        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def fetch_categories():
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'categories': format_categories(categories)
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route('/questions')
    def fetch_questions():
        ques = Question.query.all()
        len_ques = len(ques)
        paginated_result = paginate(request, ques)
        
        if not paginated_result:
            abort(404)
        try:
            categories = format_categories(Category.query.all())
            return jsonify({
                'success': True,
                'questions': paginated_result,
                'total_questions': len_ques,
                'categories': categories
            })
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(422)
        finally:
            db.session.close()

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            ques = Question.query.filter_by(id=id).one_or_none()
            if ques is None:
                abort(404)
            ques.delete()
            return jsonify({
                'success': True,
                'deleted': id
            })
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        #validate request
        if not ('question' in data and 'answer' in data and
                'difficulty' in data and 'category' in data):
            abort(422)
        #check for non-emptiness
        for i in data:
            if data[i] != '' or data[i] != None:
                pass
            else:
                abort(422)

        question = data['question']
        answer = data['answer']
        difficulty = data['difficulty']
        category = data['category']
        try:
            question = Question(question=question, answer=answer,
                                difficulty=difficulty,
                                category=category)
            question.insert()
            return jsonify({
                'success': True,
                'message': 'Question added successfully'
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/questions/search', methods=['POST'])
    def search_question(): 
        term = request.get_json().get('searchTerm', None)
        try:
            ques = Question.query.filter(Question.question.ilike(f"%{term}%")).all()
            
            if (len(ques) == 0):
                abort(404)
            
            return jsonify({
                'success': True,
                'questions': paginate(request,ques),
                'total_questions': len(ques),
                'current_category': None
            })
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    
    @app.route('/categories/<int:id>/questions')
    def fetch_category_questions(id):
        category = Category.query.filter_by(id=id).one_or_none()
        if not category:
            abort(404)
        try:
            ques = Question.query.filter_by(category=id).all()
            len_ques = len(Question.query.all())
            return jsonify({
                'success': True,
                'total_questions': len_ques,
                'questions': paginate(request, ques),
                'current_category': category.type
            })
        except Exception as e:
            print(e)
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        try:
            data = request.get_json()
            if not data:
                abort(404)
            category = data.get('quiz_category', None)
            existing_ques = data.get('previous_questions', None)
            
            if category != None:
                    pass
            else:
                abort(422)
            if category['type'] == 'click' and category['id'] == 0:
                ques = Question.query.filter(Question.id.notin_((existing_ques))).all()
            else:
                category_id = category['id']
                ques = Question.query.filter_by(category=category_id).filter(Question.id.notin_((existing_ques))).all()
            if len(ques) == None:
                    response = None
            else:
                choice = random.randrange(0, len(ques))
                res = ques[choice].format()
                return jsonify({
                    'success': True,
                    'question': res
                })
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }),400

    @app.errorhandler(404)
    def not_found_request(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found.'
        }),404

    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable request' 
        }), 422

    @app.errorhandler(500)
    def server_error_request(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500
        
    return app

