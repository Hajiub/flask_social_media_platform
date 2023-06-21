from . import search
from app.models import User
from flask import render_template, request, jsonify

@search.route('/search_root')
def search_root():
    return render_template('search/search_root.html')

@search.route('/search', methods=['POST'])
def search():
    
    keyword = request.json['keyword']
    results = User.query.filter(User.username.like(f'%{keyword}%')).all()
    return jsonify(results=[user.serialize() for user in results])
