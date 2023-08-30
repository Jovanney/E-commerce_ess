from pytest_bdd import parsers, given, when, then, scenario
from unittest.mock import Mock
import pytest
from database.models.modelos import Pedido
from database.get_db import SessionLocal

@pytest.fixture
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@scenario(scenario_name="Cancelamento bem-sucedido de um pedido confirmado", feature_name="../features/cancelamento.feature")
def test_cancelamento_pedido_confirmado():
    """ Testa cancelamento bem-sucedido de um pedido confirmado """

@pytest.fixture
def mock_query():
    return Mock()

@given(parsers.cfparse('No banco de dados, tenho um pedido de ID "{pedido_id}" associado ao CPF "{cpf}" com id_status "{status_id}"'))
def setup_mock_pedido_confirmado(mock_query, pedido_id, cpf, status_id):
    mock_pedido = Mock(id=pedido_id, cpf=cpf, id_status=status_id)
    mock_query.filter().first.return_value = mock_pedido
    return mock_query

@when(parsers.cfparse('Faço uma requisição PUT para "/cancelar_pedido/{cpf}/{pedido_id}"'))
def send_cancel_request(context, client, cpf, pedido_id, mock_query):
    context["response"] = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["db_query"] = mock_query

@then(parsers.cfparse('O servidor deve responder alterando o id_status para "{new_status}" para o pedido "{id_pedido}"'))
def check_status_update(get_db, id_pedido, new_status):
    # Consulta o pedido real no banco de dados usando a sessão
    pedido = get_db.query(Pedido).filter_by(id_pedido=id_pedido).first()
    assert pedido.pedido_status == int(new_status)

@then(parsers.cfparse('A resposta deve conter a mensagem "{message}"'))
def check_response_message(context, message):
    assert context["response"].json()["message"] == message