from models.funcionario_models import Funcionario  # Importa o modelo Funcionario
from db import db  # Importa a conexão com o banco de dados
import json
from flask import make_response, request

# Função para obter todos os funcionários
def get_funcionarios():
    funcionarios = Funcionario.query.all()  # Busca todos os funcionários no banco de dados
    
    if not funcionarios:  # Verifica se a lista de funcionários está vazia
        response = make_response(
            json.dumps({
                'mensagem': 'Nenhum funcionário encontrado.',
                'dados': []  # Nenhum funcionário encontrado
            }, ensure_ascii=False, sort_keys=False)
        )
    else:
        response = make_response(
            json.dumps({
                'mensagem': 'Lista de funcionários.',
                'dados': [funcionario.json() for funcionario in funcionarios]  # Converte os objetos de funcionário para JSON
            }, ensure_ascii=False, sort_keys=False)  # Mantém caracteres especiais corretamente formatados
        )
    
    response.headers['Content-Type'] = 'application/json'  # Define o tipo de conteúdo como JSON
    return response

# Função para obter um funcionário específico por ID
def get_funcionario_by_id(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)  # Busca o funcionário pelo ID

    if funcionario:  # Verifica se o funcionário foi encontrado
        response = make_response(
            json.dumps({
                'mensagem': 'Funcionário encontrado.',
                'dados': funcionario.json()  # Converte os dados do funcionário para formato JSON
            }, ensure_ascii=False, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'  # Garante que o tipo da resposta seja JSON
        return response
    else:
        # Se o funcionário não for encontrado, retorna erro com código 404
        response = make_response(
            json.dumps({'mensagem': 'Funcionário não encontrado.', 'dados': {}}, ensure_ascii=False),
            404  # Código HTTP 404 para "Não encontrado"
        )
        response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
        return response
    
# Função para consultar um funcionário por nome
def get_funcionario_by_nome(funcionario_nome):
    funcionario = Funcionario.query.filter_by(nome=funcionario_nome).first()  # Busca o funcionário pelo nome

    if funcionario:
        response = make_response(
            json.dumps({
                'mensagem': 'Funcionário encontrado.',
                'dados': funcionario.json()
            }, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps({
                'mensagem': 'Funcionário não encontrado.',
                'dados': {}
            }, sort_keys=False)
        )
        response.headers['Content-Type'] = 'application/json'
        return response, 404


# Função para criar um novo funcionário
def create_funcionario(funcionario_data):
    # Valida se todos os campos obrigatórios foram fornecidos
    if not all(key in funcionario_data for key in ['nome', 'cargo', 'salario']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Nome, cargo e salário são obrigatórios.'}, ensure_ascii=False),
            400  # Código HTTP 400 para requisição inválida
        )
        response.headers['Content-Type'] = 'application/json'  # Garante que a resposta seja em JSON
        return response
    
    # Se os dados forem válidos, cria o novo funcionário
    novo_funcionario = Funcionario(
        nome=funcionario_data['nome'],
        cargo=funcionario_data['cargo'],
        salario=funcionario_data['salario']
    )
    
    db.session.add(novo_funcionario)  # Adiciona o novo funcionário ao banco de dados
    db.session.commit()  # Confirma a transação no banco

    # Resposta de sucesso com os dados do novo funcionário
    response = make_response(
        json.dumps({
            'mensagem': 'Funcionário cadastrado com sucesso.',
            'funcionario': novo_funcionario.json()  # Retorna os dados do funcionário cadastrado
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
    return response

# Função para atualizar um funcionário por ID
def update_funcionario(funcionario_id, funcionario_data):
    funcionario = Funcionario.query.get(funcionario_id)  # Busca o funcionário pelo ID

    if not funcionario:  # Se o funcionário não for encontrado, retorna erro
        response = make_response(
            json.dumps({'mensagem': 'Funcionário não encontrado.'}, ensure_ascii=False),
            404  # Código HTTP 404 para "Não encontrado"
        )
        response.headers['Content-Type'] = 'application/json'  # Garante que a resposta seja em JSON
        return response

    # Valida se todos os campos obrigatórios foram fornecidos
    if not all(key in funcionario_data for key in ['nome', 'cargo', 'salario']):
        response = make_response(
            json.dumps({'mensagem': 'Dados inválidos. Nome, cargo e salário são obrigatórios.'}, ensure_ascii=False),
            400  # Código HTTP 400 para requisição inválida
        )
        response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
        return response

    # Atualiza os dados do funcionário
    funcionario.nome = funcionario_data['nome']
    funcionario.cargo = funcionario_data['cargo']
    funcionario.salario = funcionario_data['salario']

    db.session.commit()  # Confirma a atualização no banco de dados

    # Retorna a resposta com os dados do funcionário atualizado
    response = make_response(
        json.dumps({
            'mensagem': 'Funcionário atualizado com sucesso.',
            'funcionario': funcionario.json()
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'  # Define que a resposta é em JSON
    return response

# Função para excluir um funcionário por ID com confirmação via parâmetro

def delete_funcionario(funcionario_id):
    confirmacao = request.args.get('confirmacao')  # Obtém o parâmetro de confirmação da URL

    if confirmacao != 'true':  # Se a confirmação não for enviada corretamente
        response = make_response(
            json.dumps({'mensagem': 'Confirmação necessária para excluir o funcionário.'}, ensure_ascii=False),
            400  # Código HTTP 400 para "Requisição inválida"
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    funcionario = Funcionario.query.get(funcionario_id)  # Busca o funcionário pelo ID
    if not funcionario:  # Se o funcionário não for encontrado, retorna erro
        response = make_response(
            json.dumps({'mensagem': 'Funcionário não encontrado.'}, ensure_ascii=False),
            404  # Código HTTP 404 para "Não encontrado"
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    db.session.delete(funcionario)  # Remove o funcionário do banco de dados
    db.session.commit()  # Confirma a exclusão

    # Retorna a resposta com a mensagem de sucesso
    response = make_response(
        json.dumps({'mensagem': 'Funcionário excluído com sucesso.'}, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response
