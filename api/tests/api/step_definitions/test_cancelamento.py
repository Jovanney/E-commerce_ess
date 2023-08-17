from pytest_bdd import parsers, given, when, then, scenario
from api.tests.api.utils.utils import get_user_test




# Mock simples de um banco de dados em memória
class MockedDB:
    def __init__(self):
        self.orders = {}
    
    def set_order_status(self, pedido_id, cpf, status):
        self.orders[(pedido_id, cpf)] = status
    
    def get_order_status(self, pedido_id, cpf):
        return self.orders.get((pedido_id, cpf))

# Instanciação do mock
mocked_db = MockedDB()



@scenario(feature_name="../features/cancelamento.feature", scenario_name="Cancelamento de um pedido que não existe")
def test_cancel_nonexistent_order():
    pass

@given(parsers.cfparse('No banco de dados, não existe um pedido com ID "{pedido_id:d}" para o cpf "{cpf}"'))
def mock_no_order_in_db(pedido_id: int, cpf: str):
    pass  

@when(parsers.cfparse('Faço uma requisição do tipo PUT para a rota /cancelar_pedido/{cpf}/{pedido_id:d}'), target_fixture="context")
def send_cancel_request(client, context, cpf: str, pedido_id: int):
    response = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor retorna um erro com detalhe "{detail}"'), target_fixture="context")
def check_response_detail(context, detail: str):
    assert "detail" in context["response"].json()
    assert context["response"].json()["detail"] == detail
    return context


#-------------------------------------------------------------------------------------------------
@scenario(feature_name="../features/cancelamento.feature", scenario_name="Tentativa de cancelar um pedido já cancelado")
def test_cancel_already_canceled_order():
    pass

@given(parsers.cfparse('No banco de dados, tenho um pedido de ID "{pedido_id:d}" associado ao CPF "{cpf}" com status "{status:d}"'))
def mock_order_with_status(pedido_id: int, cpf: str, status: int):
    assert status == 5, "O status deve ser '5' (Cancelado)"
    mocked_db.set_order_status(pedido_id, cpf, status)

@when(parsers.cfparse('Faço uma requisição do tipo PUT para a rota /cancelar_pedido/{cpf}/{pedido_id:d}'), target_fixture="context")
def send_cancel_request(client, context, cpf: str, pedido_id: int):
    response = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor retorna um erro com detalhe "{detail}"'), target_fixture="context")
def check_response_detail(context, detail: str):
    assert "detail" in context["response"].json()
    assert context["response"].json()["detail"] == detail
    return context


#--------------------------------------------------------------------------------
from pytest_bdd import parsers, given, when, then, scenario

@scenario(feature_name="../features/cancelamento.feature", scenario_name="Cancelamento bem-sucedido de um pedido confirmado")
def test_successful_order_cancellation():
    pass

# Agora o status é esperado como um número
@given(parsers.cfparse('No banco de dados, tenho um pedido de ID "{pedido_id:d}" associado ao CPF "{cpf}" com status "{status:d}"'))
def mock_order_with_status(pedido_id: int, cpf: str, status: int):
    assert status == 2, "O status deve ser '2' (Concluído)"
    mocked_db.set_order_status(pedido_id, cpf, status)

@when(parsers.cfparse('Faço uma requisição do tipo PUT para a rota /cancelar_pedido/{cpf}/{pedido_id:d}'), target_fixture="context")
def send_cancel_request(client, context, cpf: str, pedido_id: int):
    response = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor atualiza o status do pedido para "{new_status:d}"'))
def check_order_status_in_db(pedido_id: int, cpf: str, new_status: int):
    assert mocked_db.get_order_status(pedido_id, cpf) == new_status

@then(parsers.cfparse('Retorna uma resposta com a mensagem "{message}"'), target_fixture="context")
def check_response_message(context, message: str):
    assert "message" in context["response"].json()
    assert context["response"].json()["message"] == message
    return context


#----------------------------------------------------------------
@scenario(feature_name="../features/cancelamento.feature", scenario_name="Tentativa de cancelar um pedido que não pode ser cancelado")
def test_attempt_to_cancel_non_cancellable_order():
    pass

@given(parsers.cfparse('No banco de dados, tenho um pedido de ID "{pedido_id:d}" associado ao CPF "{cpf}" com um status “{status1:d}” ou “{status2:d}”'))
def mock_order_with_non_cancellable_status(pedido_id: int, cpf: str, status1: int, status2: int):
    # Verificar que os status fornecidos são realmente 3 e 4
    assert status1 in [3, 4] and status2 in [3, 4], "Os status devem ser '3' (Em rota) ou '4' (Concluído)"
    mocked_db.set_order_status(pedido_id, cpf, status1)

@when(parsers.cfparse('Faço uma requisição do tipo PUT para a rota /cancelar_pedido/{cpf}/{pedido_id:d}'), target_fixture="context")
def send_cancel_request(client, context, cpf: str, pedido_id: int):
    response = client.put(f"/cancelar_pedido/{cpf}/{pedido_id}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor retorna um erro com detalhe "{detail}"'), target_fixture="context")
def check_response_detail(context, detail: str):
    assert "detail" in context["response"].json()
    assert context["response"].json()["detail"] == detail
    return context

