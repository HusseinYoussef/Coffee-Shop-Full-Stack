import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add(
                'Allow-Control-Allow-Headers',
                'Content-Type,Authorization,true'
                )
    response.headers.add(
                'Allow-Control-Allow-Methods',
                'GET, POST, PATCH, DELETE, OPTIONS'
                )

    return response

# db_drop_and_create_all()


# ROUTES
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    # no drinks
    if len(drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt):
    drinks = Drink.query.all()
    if len(drinks) == 0:
        # no drinks
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(jwt):
    body = request.get_json()

    # require body
    if body is None:
        abort(400)

    # get body params
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    if (title is None) or (recipe is None):
        abort(400)

    if not isinstance(recipe, list):
        abort(422)

    drink = Drink(title=title, recipe=json.dumps(recipe))
    try:
        drink.insert()
    except Exception as e:
        print(e)
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, drink_id):
    drink = Drink.query.get(drink_id)
    if drink is None:
        abort(404)

    body = request.get_json()
    # require body
    if body is None:
        abort(400)

    title = body.get('title', None)
    recipe = body.get('recipe', None)
    if title:
        drink.title = title
    if recipe:
        try:
            drink.recipe = json.dumps(recipe)
        except Exception as e:
            print(e)
            abort(400)
    try:
        drink.update()
    except Exception as e:
        print(e)
        # can't update exception
        abort(422)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    drink = Drink.query.get(drink_id)
    if drink is None:
        abort(404)

    try:
        drink.delete()
    except Exception as e:
        print(e)
        abort(422)

    return jsonify({
        'success': True,
        'delete': drink.id
    }), 200


# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Permission not allowed'
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server error'
    }), 500
