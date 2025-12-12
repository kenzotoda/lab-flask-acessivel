import pytest
from app import app, db, Tarefa

# Fixture: Configura o ambiente de teste com DB em memória (Caixa Branca)
@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Cria as tabelas
            yield client    # Executa os testes
            db.drop_all()   # Limpa o DB

# Teste Funcional (Verifica se a página carrega corretamente)
def test_index_carregamento(client):
    # Ferramenta: client.get (Simula requisição HTTP GET)
    response = client.get('/') 
    # Saída: Código 200 OK (Qualidade)
    assert response.status_code == 200
    # Saída: Verifica se o título de acessibilidade está presente (WCAG)
    assert b"Lista de Tarefas Acess" in response.data 

# Teste de Integração (Adiciona via HTTP e verifica o DB)
def test_adicionar_tarefa_e_db(client):
    # Entrada: Requisição POST para a rota de adição
    response = client.post('/adicionar', data={'titulo': 'Tarefa de Teste 1'}, follow_redirects=True)
    assert response.status_code == 200
    
    # Verificação de Saída no Banco de Dados (Caixa Branca)
    with app.app_context():
        tarefa = Tarefa.query.filter_by(titulo='Tarefa de Teste 1').first()
        assert tarefa is not None
        assert not tarefa.concluida

# Teste de Segurança/Confiabilidade (OWASP)
def test_adicionar_vazio_nao_cria_no_db(client):
    # Entrada: Envio de dado vazio
    response = client.post('/adicionar', data={'titulo': ''}, follow_redirects=True)
    # Saída: A aplicação deve retornar uma mensagem de erro
    assert b"O t\xc3\xadtulo da tarefa n\xc3\xa3o pode estar vazio." in response.data
    # Saída: O número de tarefas no DB não deve mudar
    with app.app_context():
        assert Tarefa.query.count() == 0 
