# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Endpoints

GET '/api/v1.0/categories'
GET '/api/v1.0/questions'
DELETE '/api/v1.0/questions/<query_id>'
GET '/api/v1.0/categories/<category_id>/questions'
POST '/api/v1.0/quizzes'
POST '/api/v1.0/questions'

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET 'api/v1.0/questions'
- Request Arguments: 'page'. To indicate the page, defaulting to 1 if not specified
- Response: returns a jso objet with keys: 'questions' containing all the question records but paginated to 10 records per page, 'totalQuestions' containing the number of all the questions, and 'categories' containing all the available categories.
-If the page argument is a digit out of range it responds with a 400 error status code.
Example: ```http://localhost:5000/questions

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "totalQuestions": 45
}```

DELETE '/api/v1.0/questions/<query_id>'
- Request Arguments: None
- Response: Returns a json object with one key 'deleted'
 with a value of the integer of the deleted record. If it fails it responds with a 404 error status code.
 Example: ```curl -X DELETE http://localhost:5000/questions/1
 {
    'deleted': 1
 }```

GET 'api/v1.0/categories/<category_id>/questions'
-Request Arguments:None
-Response: Returns a JSON object with the 'questions' that match the category number specified, 'totalQuestions' a number of all the questions in that category, and 'currentCategory' which is a string of the name of the category.
-If the number given is not a valid category id it responds with a 404 error status code.
Example:```http://localhost:5000/categories/2/questions
{
  "currentCategory": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "totalQuestions": 2
}```

POST '/api/v1.0/quizzes'
-Request Arguments: 'previous_questions' a list of the previous questions' ids, 'quiz_category' an integer of a category id
-Response: returns a random question record in the mentioned category but with an id that is not in the previous questions list
Example:```http://localhost:5000/quizzes  {'previous_questions':[1,2], 'quiz_category':2}
{
    'category':2,
    'question':'Who?',
    'answer': 'Me',
    'difficulty': 2
}

POST '/api/v1.0/questions'
-Request Arguments: 'searchTerm' this is a term to search for in the questions.
-Response: It performs a case insensitive search of the searchTerm on the questions and Returns a JSON object containing the keys; 'questions' all the questions that matched the searchTerm and 'totalQuestions' the number of all the questions returned
Example:```POST http://localhost:5000/questions {'searchTerm':'title'}
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ], 
  "totalQuestions": 1
}```

POST '/api/v1.0/questions'
-Request Arguments: 'question','answer','difficulty','category'
-Response: It creates a new question record and returns a JSON object with a key 'created' with a value of the id of the newly created question

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
