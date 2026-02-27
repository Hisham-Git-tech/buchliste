from flask import Blueprint

# Blueprint für die Buchliste-Funktionalität
bp = Blueprint('books', __name__)

from app.books import routes
