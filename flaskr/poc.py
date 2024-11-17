from flask import (
    Blueprint, request, jsonify
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
        'WITH q AS ( SELECT p.name, p.product_id FROM products p WHERE name LIKE ?), '
        'w AS ( SELECT *  FROM contacts c  JOIN product_contacts pc ON c.contact_id = pc.contact_id)'
        'SELECT *  FROM q  JOIN w ON q.product_id = w.product_id  WHERE w.role = ?;',
        ('%' + search_query + '%', 'Scrum Master',)
    ).fetchall()

    if not products:
        return jsonify([])

    result = [
        {
            "product name": product["name"],
            "first name": product["first_name"],
            "last name": product["last_name"],
            "email": product["email"],
            "chat username": product["chat_username"],
            "location": product["location"],
            "role": product["role"]
        }
        for product in products
    ]

    return jsonify(result)

@bp.route('/repos', methods=['GET'])
def repositories():
    print("Found")
    search_query = request.args.get('search_query', '')
    db = get_db()
    repos = db.execute(
        'SELECT r.name AS repository_name, '
        '       r.url AS repository_url, '
        '       p.name AS product_name, '
        '       c.chat_username, '
        '       c.email, '
        '       c.first_name, '
        '       c.last_name, '
        '       c.location, '
        '       c.role '
        'FROM repositories r '
        'JOIN products p ON r.product_id = p.product_id '
        'JOIN product_contacts pc ON p.product_id = pc.product_id '
        'JOIN contacts c ON pc.contact_id = c.contact_id '
        'WHERE r.name LIKE ? '
        'AND c.role = ?;',
        ('%' + search_query + '%', 'Scrum Master',)
    ).fetchall()

    if not repos:
        return jsonify([])

    result = [
        {
            "repo name": repo["repository_name"],
            "repo url": repo["repository_url"],
            "product name": repo["product_name"],
            "first name": repo["first_name"],
            "last name": repo["last_name"],
            "email": repo["email"],
            "chat username": repo["chat_username"],
            "location": repo["location"],
            "role": repo["role"]
        }
        for repo in repos
    ]
    
    return jsonify(result)