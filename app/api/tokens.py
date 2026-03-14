from flask import jsonify, request
from app import db
from app.api import bp
from app.models import User
from app.api.auth import token_auth


@bp.route('/tokens', methods=['POST'])
def get_token():
    username = None
    password = None

    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password

    if (not username or not password) and request.is_json:
        data = request.get_json(silent=True) or {}
        username = data.get('username')
        password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'missing credentials'}), 400

    user = db.session.query(User).filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'error': 'invalid credentials'}), 401

    token = user.get_token()
    db.session.commit()

    return jsonify({
        'token': token,
        'token_type': 'Bearer',
        'expires_in': 3600
    }), 200


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return jsonify({'status': 'revoked'}), 200
