from flask import request, url_for, jsonify

def paginate(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]