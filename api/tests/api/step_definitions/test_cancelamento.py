from pytest_bdd import parsers, given, when, then, scenario
from unittest.mock import Mock
import pytest
from database.models.modelos import Pedido
from database.get_db import SessionLocal


@scenario(scenario_name="Tentativa de cancelamento de um pedido inexistente", feature_name="../features/cancelamento.feature")
def test_cancelamento_inexistente():
    """ Testa cancelamento de pedido inexistente """

@pytest.fixture
def mock_query():
    return Mock()

@given(parsers.cfparse('Que não existe um pedido com ID "{pedido_id}" associado ao CPF "{cpf}" no banco de dados'))
def setup_mock_no_pedido_for_cpf(mock_query, pedido_id, cpf):
    mock_query.filter().first.return_value = None
    return mock_query

@when(parsers.cfparse('Faço uma requisição PUT para "/cancelar_pedido/{cpf}/{pedido_id}"'))
def send_cancel_request(context, client, cpf, pedido_id, mock_query):
    context["response"] = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["db_query"] = mock_query

@then(parsers.cfparse('O servidor deve responder com o status "{status_code}"'))
def check_response_status(context, status_code):
    assert context["response"].status_code == int(status_code)

@then(parsers.cfparse('A resposta deve conter o detalhe "{detail}"'))
def check_response_detail(context, detail):
    assert context["response"].json()["detail"] == detail

#---------------------------------------------------

@scenario(scenario_name="Tentativa de cancelar um pedido já cancelado", feature_name="../features/cancelamento.feature")
def test_pedido_ja_cancelado():
    """ Testa cancelamento de pedido que já foi cancelado """

@pytest.fixture
def mock_query():
    return Mock()

@given(parsers.cfparse('No banco de dados, tenho um pedido de ID "{pedido_id}" associado ao CPF "{cpf}" com id_status "{status_id}"'))
def setup_mock_pedido_cancelado(mock_query, pedido_id, cpf, status_id):
    mock_pedido = Mock(id=pedido_id, cpf=cpf, id_status=status_id)
    mock_query.filter().first.return_value = mock_pedido
    return mock_query

@when(parsers.cfparse('Faço uma requisição PUT para "/cancelar_pedido/{cpf}/{pedido_id}"'))
def send_cancel_request(context, client, cpf, pedido_id, mock_query):
    context["response"] = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["db_query"] = mock_query

@then(parsers.cfparse('O servidor deve responder com o status "{status_code}"'))
def check_response_status(context, status_code):
    assert context["response"].status_code == int(status_code)

@then(parsers.cfparse('A resposta deve conter o detalhe "{detail}"'))
def check_response_detail(context, detail):
    assert context["response"].json()["detail"] == detail

#--------------------------------------------

@scenario(
    scenario_name="Tentativa de cancelar um pedido que não pode ser cancelado",
    feature_name="../features/cancelamento.feature"
)
def test_pedido_nao_cancelavel():
    """ Testa tentativa de cancelamento de um pedido que não pode ser cancelado """

@pytest.fixture
def mock_query_2():
    return Mock()

@given(parsers.cfparse('No banco de dados, tenho um pedido de ID "{pedido_id}" associado ao CPF "{cpf}" com id_status "{status_id}"'))
def setup_mock_pedido_nao_cancelavel(mock_query_2, pedido_id, cpf, status_id):
    mock_pedido = Mock(id=pedido_id, cpf=cpf, id_status=status_id)
    mock_query_2.filter().first.return_value = mock_pedido
    return mock_query_2

@when(parsers.cfparse('Faço uma requisição PUT para "/cancelar_pedido/{cpf}/{pedido_id}"'))
def send_cancel_request_nao_cancelavel(context, client, cpf, pedido_id, mock_query_2):
    context["response"] = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["db_query_2"] = mock_query_2

@then(parsers.cfparse('O servidor deve responder com o status "{status_code}"'))
def check_response_status_nao_cancelavel(context, status_code):
    assert context["response"].status_code == int(status_code)

@then(parsers.cfparse('A resposta deve conter o detalhe "{detail}"'))
def check_response_detail_nao_cancelavel(context, detail):
    assert context["response"].json()["detail"] == detail



