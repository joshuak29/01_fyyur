from ast import Or
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#The below paginate will be called to return paginated questions
def paginate(request, resource):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  
  questions = [question.format() for question in resource]
  return questions[start:end]

#This returns all categories as a dictionary of id: type key: value pairs
def all_categories(category):
  categories_all = [cat.format() for cat in category]
  categories = {}
  for i in categories_all:
    categories[i['id']] = i['type']
  
  return categories

def quiz(questions, previous):
  next_questions = []
  question_ids = [question['category'] for question in questions]
  
  for i in questions:
    if i['id'] in previous:
      continue
    else:
      next_questions.append(i)
  
  return next_questions
  
    
  


  
  

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}}) # allow all resources to access my api
  

  @app.after_request         #a function under this decorator is run after every request
  def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"     #allow certain headers and 
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"  #A NUMBER OF REQUESTS THAT ARE ALLOWED from the resources
        )
        return response

  
  

 # endpoint that returns all the categories throug GET reqquests 
  @app.route('/categories')     
  def get_categories():
    category = Category.query.all()
    
    try:
      if len(all_categories(category)) == 0:
        abort(422)
        
      
        
      return jsonify({
        'categories': all_categories(category)
      })
    except:
      abort(422)                #return 422 unproccessable error if request fails
      
        
      
      
#This endpoint returns a list of questions, number of total questions, current category, categories. 
# Throug a GET request with page argument to indicate the page
# Returning a 400 error when the page is out of range

  @app.route('/questions')      
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    
    try:
      current_questions = paginate(request, questions)
      if len(current_questions) == 0:
        abort(400)
        
      
      return jsonify({
        'questions': paginate(request, questions),
        'totalQuestions': len(questions),
        'categories': all_categories(categories)
      })
    except:
      abort(400)        


  
  
  # This endpoint sends a DELETE request to delette a question using a question ID. 
  @app.route('/questions/<int:query_id>', methods=['DELETE'])
  def delete_question(query_id):
    query = Question.query.filter(Question.id == query_id).one_or_none()
    
    if query == None:
      abort(404)
    try:
      query.delete()
      
      return jsonify({
        'deleted': query_id
      })
    except:
      abort(404)

 
  # This endpoint  accepts a POST request with arguments  question, answer, category, and difficulty to create a new question.
  
  # If their is a searchTerm argument in the request it responses with all the question records that match 
  # The searchTerm with a case insensitive query
  
  # If non of the above arguments is found it returns a 400 error
  @app.route('/questions', methods=['POST'])
  def add_question():
    
    new_question = request.args.get("question", None, type=str)
    new_answer = request.args.get("answer", None, type=str)
    new_difficulty = request.args.get("difficulty", None, type=str)
    new_category = request.args.get("category", None, type=int)
    search_term = request.args.get("searchTerm", None, type=str)
    
    try:
      if search_term is None:
        if new_question or new_answer or new_category or new_difficulty is None:
          abort(400)
        else:
          question1 = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
          
          question1.insert()
          return search_term
      
      else:
        results = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
        queries = [query.format() for query in results]
        
        return jsonify({
          'questions': queries,
          'totalQuestions': len(queries)
        })
    except Exception as e:
      print(e)
      abort(400)
   


  # This enpoint Create a GET request to get questions based on category. 
  @app.route('/categories/<int:category_id>/questions')
  def get_query_by_category(category_id):
    
    questions = Question.query.filter(Question.category == category_id).all()
    
    try:
      category = Category.query.filter(Category.id == category_id).one_or_none().format()
      return jsonify({
        'questions': [x.format() for x in questions],
        'totalQuestions': len(questions),
        'currentCategory':category['type']
      })
      
    except:
      abort(404)
    




  # This endpoint Creates a POST to get questions to play the quiz.
  # It takes category and previous question parameters and return a random question within the given category, 
  #if provided, and that is not one of the previous questions. 
  
  @app.route('/quizzes', methods=(['POST']))
  def post_next_question():
    try:
      previous_questions = request.args.get('previous_questions', type=list)
      category = request.args.get('quiz_category', type=int)
      
      category_id = Category.query.filter(Category.type == category).one_or_none().format()['id']
      query = Question.query.filter(Question.category == category_id).all()
      
      questions = [question.format() for question in query]
      
      valid_questions = quiz(questions, previous_questions)
      question = random.choice(valid_questions)
      
      return question
    except Exception as e:
      print(e) 
      abort(400)
      
  
    
    
  
      
      
      
      
  
#Below are the error handlers for different errors a user might encounter
  @app.errorhandler(404)
  def not_found(error):
    return (
        jsonify({"error": 404, "message": "resource not found"}),
        404,
    )
  
  @app.errorhandler(422)
  def unprocessable(error):
    
    return (
        jsonify({"error": 422, "message": "unprocessable"}),
        422,
    )

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({"error": 400, "message": "bad request"}), 400

  @app.errorhandler(405)
  def not_found(error):
      return (
          jsonify({"error": 405, "message": "method not allowed"}),
          405,
      )
  
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'error': 500, 'message':'server error'
    })
  
  return app

    