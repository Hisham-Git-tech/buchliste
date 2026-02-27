import sqlalchemy as sa
from flask import jsonify, request
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Book


@bp.route('/books', methods=['GET'])
@token_auth.login_required
def get_books():
    """Alle Bücher des authentifizierten Benutzers zurückgeben."""
    user = token_auth.current_user()
    status = request.args.get('status')
    query = sa.select(Book).where(Book.user_id == user.id).order_by(Book.timestamp.desc())
    if status:
        query = sa.select(Book).where(
            Book.user_id == user.id,
            Book.status == status
        ).order_by(Book.timestamp.desc())
    books = db.session.scalars(query).all()
    return jsonify({'items': [b.to_dict() for b in books], 'total': len(books)})


@bp.route('/books/<int:id>', methods=['GET'])
@token_auth.login_required
def get_book(id):
    """Ein einzelnes Buch anhand der ID zurückgeben."""
    book = db.get_or_404(Book, id)
    return jsonify(book.to_dict())


@bp.route('/books', methods=['POST'])
@token_auth.login_required
def create_book():
    """Neues Buch für den authentifizierten Benutzer erstellen."""
    user = token_auth.current_user()
    data = request.get_json() or {}
    if 'title' not in data or 'author' not in data:
        return bad_request('Titel und Autor sind erforderlich.')
    valid_statuses = ['want_to_read', 'reading', 'read']
    if 'status' in data and data['status'] not in valid_statuses:
        return bad_request(f'Status muss einer von {valid_statuses} sein.')
    rating = data.get('rating', 0)
    if not isinstance(rating, int) or rating < 0 or rating > 5:
        return bad_request('Bewertung muss eine Zahl zwischen 0 und 5 sein.')
    book = Book(
        title=data['title'],
        author=data['author'],
        genre=data.get('genre', 'other'),
        status=data.get('status', 'want_to_read'),
        rating=rating,
        found_via=data.get('found_via'),
        notes=data.get('notes', ''),
        user_id=user.id
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201


@bp.route('/books/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_book(id):
    """Buch aktualisieren (nur eigene Bücher)."""
    user = token_auth.current_user()
    book = db.get_or_404(Book, id)
    if book.user_id != user.id:
        return bad_request('Dieses Buch gehört dir nicht.')
    data = request.get_json() or {}
    for field in ['title', 'author', 'genre', 'status', 'found_via', 'notes']:
        if field in data:
            setattr(book, field, data[field])
    if 'rating' in data:
        rating = data['rating']
        if not isinstance(rating, int) or rating < 0 or rating > 5:
            return bad_request('Bewertung muss eine Zahl zwischen 0 und 5 sein.')
        book.rating = rating
    db.session.commit()
    return jsonify(book.to_dict())


@bp.route('/books/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_book(id):
    """Buch löschen (nur eigene Bücher)."""
    user = token_auth.current_user()
    book = db.get_or_404(Book, id)
    if book.user_id != user.id:
        return bad_request('Dieses Buch gehört dir nicht.')
    db.session.delete(book)
    db.session.commit()
    return '', 204
