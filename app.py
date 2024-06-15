from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)

oauth.register(
    name='keycloak',
    client_id=app.config['OAUTH2_CLIENT_ID'],
    client_secret=app.config['OAUTH2_CLIENT_SECRET'],
    server_metadata_url=app.config['OAUTH2_DISCOVERY_URL'],
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.keycloak.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.keycloak.authorize_access_token()
    user = oauth.keycloak.parse_id_token(token)
    session['user'] = user
    return redirect('/')

@app.route('/desbloquear/<username>', methods=['PUT'])
def desbloquear_usuario(username):
    user = User.query.filter_by(username=username).first()
    if user and user.bloqueado:
        user.bloqueado = False
        db.session.commit()
        return jsonify({"message": "Usuário desbloqueado com sucesso!"}), 200
    return jsonify({"message": "Usuário não encontrado ou não bloqueado."}), 404

if __name__ == '__main__':
    app.run()
