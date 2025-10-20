from flask import Blueprint, request 
from controllers.funcionario_controllers import (
    get_funcionarios,
    get_funcionario_by_id,
    get_funcionario_by_nome,
    create_funcionario,
    update_funcionario,
    delete_funcionario
)
# Define um Blueprint para as rotas de "Funcionario"
funcionario_routes = Blueprint('funcionario_routes', __name__)  

# Rota para listar todos os funcionários (GET)
@funcionario_routes.route('/Funcionario', methods=['GET'])
def funcionarios_get():
    return get_funcionarios()

# Rota para buscar um funcionário pelo ID (GET)
@funcionario_routes.route('/Funcionario/<int:funcionario_id>', methods=['GET'])
def funcionario_get_by_id(funcionario_id):
    return get_funcionario_by_id(funcionario_id)

@funcionario_routes.route('/Funcionario/<string:funcionario_nome>', methods=['GET'])  # Alterado para consulta por nome
def funcionario_get_by_nome(funcionario_nome):  # Alterado para buscar por nome
    return get_funcionario_by_nome(funcionario_nome)  # Alterado para chamar a função que usa o nome

# Rota para criar um novo funcionário (POST)
@funcionario_routes.route('/Funcionario', methods=['POST'])
def funcionarios_post():
    return create_funcionario(request.json)

# Rota para atualizar um funcionário pelo ID (PUT)
@funcionario_routes.route('/Funcionario/<int:funcionario_id>', methods=['PUT'])
def funcionarios_put(funcionario_id):
    return update_funcionario(funcionario_id, request.json)

# Rota para excluir um funcionário pelo ID (DELETE)
@funcionario_routes.route('/Funcionario/<int:funcionario_id>', methods=['DELETE'])
def funcionario_delete(funcionario_id):
    return delete_funcionario(funcionario_id)
