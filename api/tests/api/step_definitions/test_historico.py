from pytest_bdd import parsers, given, when, then, scenario
from api.tests.api.utils.utils import get_user_test

@scenario(feature_name="../features/historico_pedidos.feature", scenario_name="Usuário acessando histórico e não encontrando nenhum pedido")
def test_user_no_order_history():
    pass

@given(parsers.cfparse('Sou um Usuario registrado no sistema com o cpf igual a "{cpf}"'))
def mock_user_response(cpf: str):
    user = get_user_test(cpf=cpf)

@given('No banco de dados, não tenho nenhum Pedido associado ao meu cpf')
def mock_no_orders_for_user():
    pass  

@when(parsers.cfparse('Faço uma requisição do tipo GET para a rota /pedidos/{cpf}'), target_fixture="context")
def send_order_history_request(client, context, cpf: str):
    response = client.get(f"/pedidos/{cpf}/")
    context["response"] = response
    return context

@then(parsers.cfparse('o servidor retorna o histórico de pedidos do usuário de cpf "{cpf}"'))
def check_order_history_response(context, cpf: str):
    pass

@then(parsers.cfparse('Recebo uma resposta indicando "{message}"'), target_fixture="context")
def check_response_message(context, message: str):
    assert "detail" in context["response"].json()
    assert context["response"].json()["detail"] == message
    return context

#-----------------------------------------------------------------------------------------------------------------------------

from pytest_bdd import parsers, given, when, then, scenario
from api.tests.api.utils.utils import get_user_test

@scenario(feature_name="../features/historico_pedidos.feature", scenario_name="Usuário acessando histórico de pedidos")
def test_user_order_details():
    pass

@given(parsers.cfparse('Sou um usuário registrado no sistema com o cpf "{cpf}"'))
def mock_user_response(cpf: str):
    user = get_user_test(cpf=cpf)

@given(parsers.cfparse('No banco de dados, existe um pedido com ID "{pedido_id:d}" para o cpf "{cpf}", preço total de "{preco_total:f}" e status diferente de "{status}"'))
def mock_order_for_user(cpf: str, pedido_id: int, preco_total: float, status: str):
    pass  # Implemente a lógica para garantir a existência deste pedido no banco de dados de teste.

@given(parsers.cfparse('Associado a esse pedido, temos um item com quantidade "{quantidade:d}" e nome_produto "{nome_produto}"'))
def mock_item_for_order(quantidade: int, nome_produto: str):
    pass  # Implemente a lógica para garantir a existência deste item associado ao pedido no banco de dados de teste.

@when(parsers.cfparse('Faço uma requisição do tipo GET para a rota /pedidos/{cpf}'), target_fixture="context")
def send_order_details_request(client, context, cpf: str):
    response = client.get(f"/pedidos/{cpf}/")
    context["response"] = response
    return context

@then(parsers.cfparse('Vejo os detalhes do pedido com ID "{pedido_id:d}", preço total de "{preco_total:f}", e a lista de itens associados, incluindo um item com quantidade "{quantidade:d}" e nome "{nome_produto}"'))
def check_order_details_response(context, pedido_id: int, preco_total: float, quantidade: int, nome_produto: str):
    json_response = context["response"].json()
    # Encontre os detalhes específicos do pedido na resposta.
    order_details = next(order for order in json_response["orders"] if order["id_pedido"] == pedido_id)

    # Verificar os detalhes básicos do pedido
    assert order_details["id_pedido"] == pedido_id
    assert order_details["preco_total"] == preco_total

    # Verificar os detalhes do produto associado ao pedido
    product = next(item for item in order_details["items"] if item["nome_produto"] == nome_produto)
    assert product["quantidade"] == quantidade
    assert product["nome_produto"] == nome_produto



#------------------------------------------------------------------------------------------------------------------
from pytest_bdd import parsers, given, when, then, scenario
from api.tests.api.utils.utils import get_user_test

@scenario(feature_name="../features/historico_pedidos.feature", scenario_name="Retornar detalhes de múltiplos pedidos confirmados de um cliente")
def test_multiple_user_order_details():
    pass

@given(parsers.cfparse('Sou um usuário registrado no sistema com o cpf "{cpf}"'))
def mock_user_response(cpf: str):
    user = get_user_test(cpf=cpf)
    # Implement logic to add the user to the test database, if necessary.

@given(parsers.cfparse('No banco de dados, existe um pedido com ID "{pedido_id:d}" para o cpf "{cpf}", preço total de "{preco_total:f}" e status diferente de "{status}"'))
def mock_order_for_user(cpf: str, pedido_id: int, preco_total: float, status: str):
    # Implement logic to ensure this order exists in the test database.
    pass

@given(parsers.cfparse('Associado a esse pedido com ID "{pedido_id:d}", temos um item com quantidade "{quantidade:d}" e nome_produto "{nome_produto}"'))
def mock_item_for_order(pedido_id: int, quantidade: int, nome_produto: str):
    # Implement logic to ensure this item is associated with the given order in the test database.
    pass

@when(parsers.cfparse('Faço uma requisição do tipo GET para a rota /pedidos/{cpf}'), target_fixture="context")
def send_multiple_order_details_request(client, context, cpf: str):
    response = client.get(f"/pedidos/{cpf}/")
    context["response"] = response
    return context

@then(parsers.cfparse('Vejo os detalhes do pedido com ID "{pedido_id:d}", preço total de "{preco_total:f}", e a lista de itens associados, incluindo um item com quantidade "{quantidade:d}" e nome "{nome_produto}"'))
def check_order_details_response(context, pedido_id: int, preco_total: float, quantidade: int, nome_produto: str):
    json_response = context["response"].json()

    # Encontre os detalhes específicos do pedido na resposta.
    order_details = next(order for order in json_response["orders"] if order["id_pedido"] == pedido_id)

    # Verificar os detalhes básicos do pedido
    assert order_details["id_pedido"] == pedido_id
    assert order_details["preco_total"] == preco_total

    # Verificar os detalhes do produto associado ao pedido
    product = next(item for item in order_details["items"] if item["nome_produto"] == nome_produto)
    assert product["quantidade"] == quantidade
    assert product["nome_produto"] == nome_produto

    
    
    
    
    
    
    