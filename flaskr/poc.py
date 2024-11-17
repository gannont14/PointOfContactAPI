from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import json

bp = Blueprint('poc', __name__, url_prefix="/contact")


@bp.route('/products', methods=['GET'])
def products():
    print("Found")
    search_query = request.args.get('search_query', '')
    db = get_db()
    products = db.execute(
        'WITH q AS ('
        'SELECT p.name, p.product_id '
        'FROM products p '
        'WHERE name LIKE ?'
        '), w AS ('
        'SELECT * '
        'FROM contacts c '
        'JOIN product_contacts pc ON c.contact_id = pc.contact_id'
        ')'
        'SELECT * '
        'FROM q '
        'JOIN w ON q.product_id = w.product_id '
        'WHERE w.role = ?;',
        ('%' + search_query + '%', 'Scrum Master',)
    ).fetchall()

    if products is None:
        abort(404, "products don't exists")

    result = [
        {
            "product name": product["name"],
            "first_name": product["first_name"],
            "last_name": product["last_name"],
            "email": product["email"],
            "chat username": product["chat_username"],
            "location": product["location"],
            "role": product["role"]
        }
        for product in products
    ]

    return jsonify(result)


@bp.route('/repos', methods=['GET'])
def repos():
    print("Found")
    db = get_db()
    repos = db.execute(
        'SELECT * FROM repositories;'
    ).fetchone()

    if repos is None:
        print("No")
        abort(404, "repositories don't exists")

    return repos['name']
