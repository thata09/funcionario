from flask import Flask  # Importa o Flask
from db import db  # Importa a conexão com o banco de dados
from routes.funcionario_routes import funcionario_routes  # Importa as rotas de "Funcionario"

app = Flask(__name__)  # Inicializa o app Flask

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa o banco de dados com o app

# Registra as rotas de "Funcionario"
app.register_blueprint(funcionario_routes)

if __name__ == '__main__':
    # Cria as tabelas no banco de dados antes de iniciar o servidor
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)  # Inicia o servidor Flask
