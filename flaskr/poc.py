from flask import (
    Blueprint, request, jsonify
)
import heapq
from fuzzywuzzy import fuzz
from flaskr.db import get_db
from typing import Dict, Any, List

bp = Blueprint('poc', __name__, url_prefix="/contact")


class fuzzyHeap:
    def __init__(self):
        self.heap = []
        self.counter = 0

    def push(self, item: Dict[str, Any], search_query, dictKey):
        ratio = -fuzz.ratio(search_query.lower(), item[dictKey].lower())
        self.counter += 1
        heapq.heappush(self.heap, (ratio, self.counter, item))

    def pop(self) -> Dict[str, Any]:
        if self.heap:
            val = heapq.heappop(self.heap)
            # print(f"ratio: {val[0]}")
            return val[2]
        return None

    def get_sorted_results(self) -> List[Dict[str, Any]]:
        sorted_results = []
        while self.heap:
            sorted_results.append(self.pop())
        return sorted_results


@bp.route('/products', methods=['GET'])
def products():
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

    product_heap = fuzzyHeap()

    for product in products:
        product_dict = {
            "product name": product["name"],
            "first name": product["first_name"],
            "last name": product["last_name"],
            "email": product["email"],
            "chat username": product["chat_username"],
            "location": product["location"],
            "role": product["role"]}

        ratio = fuzz.ratio(search_query.lower(), product_dict["product name"].lower())

        min_ratio = 0.5
        if ratio >= min_ratio:
            product_heap.push(product_dict, search_query, "product name")

    result = product_heap.get_sorted_results()
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

    repo_heap = fuzzyHeap()

    for repo in repos:
        repo_dict = {
            "repo name": repo["repository_name"],
            "repo url": repo["repository_url"],
            "product name": repo["product_name"],
            "first name": repo["first_name"],
            "last name": repo["last_name"],
            "email": repo["email"],
            "chat username": repo["chat_username"],
            "location": repo["location"],
            "role": repo["role"]}

        ratio = fuzz.ratio(search_query.lower(), repo_dict["repo name"].lower())
        # print(f"Ratio: {ratio} for repo Name: {repo_dict['repo name']}")

        min_ratio = 0.5
        if ratio >= min_ratio:
            repo_heap.push(repo_dict, search_query, "repo name")

    result = repo_heap.get_sorted_results()

    return jsonify(result)


@bp.route('/products/all_contacts', methods=['GET'])
def all_contacts():
    print(f"full args: {request.args}")
    product_name = request.args.get('product_name', '')
    print(f"searching with product name: {product_name}")
    db = get_db()
    contacts = db.execute(
        'WITH q AS ( SELECT p.name, p.product_id FROM products p WHERE p.name LIKE ? ), '
        'w AS ( SELECT *  FROM contacts c  JOIN product_contacts pc ON c.contact_id = pc.contact_id)'
        'SELECT *  FROM q  JOIN w ON q.product_id = w.product_id;',
        ('%' + product_name + '%',)
    ).fetchall()

    result = [
        {
            "product name": contact["name"],
            "first name": contact["first_name"],
            "last name": contact["last_name"],
            "email": contact["email"],
            "chat username": contact["chat_username"],
            "location": contact["location"],
            "role": contact["role"]
        }
        for contact in contacts
    ]
    print(len(result))

    return jsonify(result)


@bp.route('/search/products', methods=['GET'])
def search_products():
    search_query = request.args.get('search_query', '')
    db = get_db()
    products = db.execute(
        'SELECT DISTINCT name FROM products WHERE name LIKE ? LIMIT 10',
        ('%' + search_query + '%',)
    ).fetchall()
    
    return jsonify([product['name'] for product in products])

@bp.route('/search/repos', methods=['GET'])
def search_repos():
    search_query = request.args.get('search_query', '')
    db = get_db()
    repos = db.execute(
        'SELECT DISTINCT name FROM repositories WHERE name LIKE ? LIMIT 10',
        ('%' + search_query + '%',)
    ).fetchall()
    
    return jsonify([repo['name'] for repo in repos])