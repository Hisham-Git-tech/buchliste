import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
from app import db
from app.books import bp
from app.books.forms import BookForm
from app.models import Book


@bp.route('/')
@bp.route('/books')
@login_required
def index():
    status_filter = request.args.get('status', 'all')
    query = sa.select(Book).where(Book.user_id == current_user.id).order_by(Book.timestamp.desc())

    if status_filter != 'all':
        query = sa.select(Book).where(
            Book.user_id == current_user.id,
            Book.status == status_filter
        ).order_by(Book.timestamp.desc())

    books = db.session.scalars(query).all()

    read_books = [b for b in books if b.status == 'read']
    rated_books = [b for b in read_books if b.rating and b.rating > 0]
    avg_rating = round(sum(b.rating for b in rated_books) / len(rated_books), 1) if rated_books else 0

    stats = {
        'total': len(books),
        'read': sum(1 for b in books if b.status == 'read'),
        'reading': sum(1 for b in books if b.status == 'reading'),
        'want_to_read': sum(1 for b in books if b.status == 'want_to_read'),
        'avg_rating': avg_rating
    }

    return render_template('books/index.html',
                           title='Meine Buchliste',
                           books=books,
                           stats=stats,
                           status_filter=status_filter)


@bp.route('/books/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data,
            status=form.status.data,
            rating=int(form.rating.data),
            found_via=form.found_via.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(book)
        db.session.commit()
        flash(f'Buch "{book.title}" wurde hinzugefügt!')
        return redirect(url_for('books.index'))
    return render_template('books/form.html', title='Buch hinzufügen', form=form)


@bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    book = db.get_or_404(Book, id)
    if book.user_id != current_user.id:
        abort(403)
    form = BookForm(obj=book)
    form.rating.data = str(book.rating) if book.rating else '0'
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.genre = form.genre.data
        book.status = form.status.data
        book.rating = int(form.rating.data)
        book.found_via = form.found_via.data
        book.notes = form.notes.data
        db.session.commit()
        flash(f'Buch "{book.title}" wurde aktualisiert!')
        return redirect(url_for('books.index'))
    return render_template('books/form.html', title='Buch bearbeiten', form=form, book=book)


@bp.route('/books/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    book = db.get_or_404(Book, id)
    if book.user_id != current_user.id:
        abort(403)
    db.session.delete(book)
    db.session.commit()
    flash(f'Buch "{book.title}" wurde gelöscht.')
    return redirect(url_for('books.index'))
