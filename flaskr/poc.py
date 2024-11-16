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
        'SELECT name FROM products WHERE name LIKE ?',
        ('%' + search_query + '%',)
    ).fetchall()

    if products is None:
        abort(404, "products don't exists")
    product_names = [product['name'] for product in products]
    return jsonify(product_names)


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
