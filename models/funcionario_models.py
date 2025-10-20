# Importa o objeto `db` que representa a conexão com o banco de dados
from db import db

# Define a classe Funcionario como um modelo de dados do SQLAlchemy
class Funcionario(db.Model):
    # Define o nome da tabela no banco de dados
    __tablename__ = 'funcionarios'

    # Define a estrutura da tabela com suas colunas
    id = db.Column(db.Integer, primary_key=True)  # Coluna ID, chave primária
    nome = db.Column(db.String(100), nullable=False)  # Coluna para o nome do funcionário, não pode ser nula
    cargo = db.Column(db.String(100), nullable=False)  # Coluna para o cargo do funcionário, não pode ser nula
    salario = db.Column(db.Float, nullable=False)  # Coluna para o salário do funcionário, não pode ser nula

    # Método para converter o objeto em um formato JSON
    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            'salario': self.salario
        }
