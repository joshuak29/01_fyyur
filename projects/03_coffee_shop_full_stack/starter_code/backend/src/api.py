import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    try:
        query = Drink.query.all()
        drinks = [r.short() for r in query]
        
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        print(e)
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks')
def get_drinks_detail():
    try:
        query = Drink.query.all()
        drinks = [r.long() for r in query]
        
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        print(e)
        abort(404)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks():
    body = request.get_json()
    try:
        title = body.get('title')
        recipe = body.get('recipe')

        drink1 = Drink(title=title, recipe=recipe)
        drink1.insert()
        
        return jsonify({
            'success': True,
            'drinks': drink1.long()
        })
    except Exception as e:
        print(e)
        abort(400)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(id):
    drink = Drink.query(Drink.id == id).one_or_none()
    body = request.get_json()
    try:
        if not drink:
            abort(404)
            
        title = body.get('title')
        recipe = body.get('recipe')

        drink.title = title
        drink.recipe = recipe
        
        drink.update()
        
        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except Exception as e:
        print(e)
        abort(404)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    try:
        if not drink:
            abort(404)
        
        drink.delete()
        
        return jsonify({
            'success':True,
            'deleted': id
        })
    except Exception as e:
        print(e) 
        abort(404)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
    
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404
    
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400



'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
# https://lil-6blvck.us.auth0.com/authorize?response_type=token&client_id=eo0JYGxVR0rC41nTYmTRrqPYIpjDKdoF&redirect_uri=http://localhost:8100

# https://lil-6blvck.us.auth0.com/.well-known/jwks.json
#https://lil-6blvck.us.auth0.com/authorize?response_type=token&client_id=eo0JYGxVR0rC41nTYmTRrqPYIpjDKdoF&redirect_uri=http://localhost:8100&audience=

barista_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZnNUw0SFN0Sm1VQl8wMTNaa3p5ayJ9.eyJpc3MiOiJodHRwczovL2xpbC02Ymx2Y2sudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyYzgyMDQxOTkyOWViNjNkYmNjNGNkMSIsImF1ZCI6Imh0dHBzOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2NTc4MTg3NjYsImV4cCI6MTY1NzkwNTE2NiwiYXpwIjoiZW8wSllHeFZSMHJDNDFuVFltVFJycVBZSXBqREtkb0YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MiXX0.N7E5rQJthYfnCvTb1Xx2zgiFFGv8EwdMI1Qneq6q6mto8ieunSmCBhU0mjJ0pyCu4hD3yFe49X8XEzoabvYGvHZs4p6uStzh3EoRMQa8BiLerRS7GkcpjmBYGwPTg9pEbJmbYKZBFikv_14wZnDJo74Lt52wv8pNrGTZKL9kNNI-AFX5ShGa_izb3i_XZAyefFJpsw96qxJq-cACUCvqaQXWP44616xPdiD0fMLCH6YHIk_NiRQDxWBL2Dv1hFbVwO8b_coyL8seP_9FxTDAQGqV8MzaYkzjnsW9IF9F8cmURlNPEWmCQOBgtHqEXuVT5teVBfRwzC0tAV2qKevFig'
manager_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZnNUw0SFN0Sm1VQl8wMTNaa3p5ayJ9.eyJpc3MiOiJodHRwczovL2xpbC02Ymx2Y2sudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyYzgzMjUxZjJjNzM1NzEzYWVlYzE4MSIsImF1ZCI6Imh0dHBzOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2NTc4ODQ1NzAsImV4cCI6MTY1Nzk3MDk3MCwiYXpwIjoiZW8wSllHeFZSMHJDNDFuVFltVFJycVBZSXBqREtkb0YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.iH3cB8o8T5FzdjNjySnno0UmOkc15pceodKc83LqQ-7FTE_dT7UyM8jIoGApO7BpYq2dg8UErmmbObr3EuOZyO57M9I3o9oWEmc0wlMSko7ybLwjb3jL_5bWXNj_ldW1DKojE9pSv8OhM_gePVuJNboQcBRi9d-TeWaDBkD36wiwCvdBkn78Y5WGH-j1N1vyNvlcN1C7xBa0mwfBvnQB4LGr-lj_J1MPT89YxxI5Ro56uHu3DVT08j1l9tuUmVMy4ky6UFoKpFMf4hj_5IoEYzcXbnqvzt2IJDo9NcVOJeJmQdjWSHEt4f5V4_w7qv91e1rte7ak-r-3pQrbx1SJeA'
Authority = "https://lil-6blvck.us.auth0.com/"
Audience = "http://localhost:5000"



#lil-6blvck.us.auth0.com/authorize?response_type=token&client_id=eo0JYGxVR0rC41nTYmTRrqPYIpjDKdoF&redirect_uri=http://localhost:8100&audience=https://localhost:5000