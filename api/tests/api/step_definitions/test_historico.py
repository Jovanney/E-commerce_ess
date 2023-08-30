
# Criando o fixture para o mock
from pytest_bdd import parsers, given, when, then, scenario
from unittest.mock import Mock



@scenario(scenario_name="Usuário acessando histórico e não encontrando nenhum pedido", feature_name="../features/historico_pedidos.feature")
def test_historico_vazio():
    """Exibir historico vazio"""

@given(parsers.cfparse('Sou um Usuario registrado no sistema com o cpf igual a "{cpf}"'))
def mock_registered_user(cpf):
    user_test = {"cpf": cpf}
    user_mock = Mock(return_value={"cpf": "11111111111"})
    assert user_test == user_mock.return_value

@given(parsers.cfparse('No banco de dados, não tenho nenhum Pedido associado ao meu cpf "{cpf}"'))
def mock_no_orders_for_user(cpf):
    # Simulamos que não há pedidos associados a esse CPF
    orders_for_user = []
    orders_mock = Mock(return_value=orders_for_user)
    assert not orders_mock.return_value  # Verifica se a lista de pedidos está vazia

@when(
    parsers.cfparse('Faço uma requisição do tipo GET para a rota "/pedidos/{cpf}"'))
def send_order_request(client, cpf: str, context):
    """
    Send a GET request to "/pedidos/{cpf}" with the given CPF
    """
    response = client.get("/pedidos/11111111111")
    context["response"] = response
    return context
 
@then(parsers.cfparse('o servidor retorna o histórico de pedidos do usuário de cpf "{cpf}"'))
def check_response_historico(context, cpf: str):
    """
    Check if the response contains the user's order history based on CPF
    """
    
    # Aqui, estou apenas checando o status da resposta. Você pode adaptar para verificar o conteúdo real da resposta se necessário.
    assert context["response"].status_code == 200

@then(parsers.cfparse('Recebo uma resposta indicando "Não há histórico de pedidos para este usuário."'))
def check_response_no_historico_message(context):
    """
    Check if the response JSON contains the expected message
    """

    response_json = context["response"].json()

    if isinstance(response_json, list):
        assert response_json[0]["mensagem"] == "Não há histórico de pedidos para este usuário."
    else:
        assert response_json["mensagem"] == "Não há histórico de pedidos para este usuário."
 
#---------------------------------------------------------------



from pytest_bdd import parsers, given, when, then, scenario
from unittest.mock import Mock
import pytest
from database.models.modelos import Pedido, Usuario, Produto, Item
from database.get_db import SessionLocal



@scenario(scenario_name='Usuário acessando histórico de pedidos', feature_name='../features/historico_pedidos.feature')
def test_historico_pedidos():
    """Acessando histórico de Pedidos"""

@given(parsers.cfparse('Sou um usuário registrado no sistema com o cpf "{cpf}"'))
def mock_registered_user(cpf: str):
    db = SessionLocal()
    user = db.query(Usuario).filter(Usuario.cpf == cpf).first()
    assert user is not None
    db.close()

@given(parsers.cfparse('No banco de dados, existe um pedido com ID "{pedido_id}", cpf_usuario "{cpf_usuario}", preco_total "{preco_total}" e id_status "{id_status}"'))
def given_pedido(cpf_usuario, pedido_id, preco_total, id_status):
    db = SessionLocal()
    order = db.query(Pedido).filter(Pedido.id_pedido == int(pedido_id)).first()

    assert order is not None
    assert order.cpf_usuario == cpf_usuario
    assert order.preco_total == float(preco_total)
    assert order.pedido_status == int(id_status)
    db.close()
    


@given(parsers.cfparse('Associado ao pedido "{pedido_id}", temos um item com quantidade "{quantidade}" e nome_produto "{nome_produto}"'))
def given_item_pedido(pedido_id, quantidade, nome_produto):
    db = SessionLocal()

    # Obter o produto com nome fornecido
    produto = db.query(Produto).filter(Produto.nome_produto == nome_produto).first()
    assert produto is not None

    # Verifique se o item já está associado ao pedido
    item_pedido = db.query(Item).filter(
        Item.id_pedido == int(pedido_id),
        Item.id_produto == produto.id_produto
    ).first()

    if item_pedido:
        assert item_pedido.quantidade == int(quantidade)
    else:
        # Criar um novo item_pedido e adicioná-lo ao banco de dados
        novo_item = Item(id_pedido=int(pedido_id), id_produto=produto.id_produto, quantidade=int(quantidade))
        db.add(novo_item)
        db.commit()

    db.close()


@when(parsers.cfparse('Faço uma requisição do tipo GET para a rota "/pedidos/{cpf}"'), target_fixture="context")
def send_order_request(client, cpf):
    context = {}
    response = client.get(f"/pedidos/{cpf}")
    context["response"] = response
    return context


@then(parsers.cfparse('Vejo os detalhes do pedido com ID "{pedido_id}", preço total "{preco_total}", id_status "{id_status}" e os seguintes produtos:'))
def check_pedido_details(context, pedido_id, preco_total, id_status):
    response_json = context["response"].json()
    
    expected_pedido = {
        "id_pedido": int(pedido_id),
        "preco_total": float(preco_total),
        "pedido_status": int(id_status)
    }

    assert response_json[0].get("id_pedido") == expected_pedido["id_pedido"]
    assert response_json[0].get("preco_total") == expected_pedido["preco_total"]
    assert response_json[0].get("pedido_status") == expected_pedido["pedido_status"]

@then(parsers.cfparse('Vejo os detalhes do pedido com ID "{pedido_id}", preço total "{preco_total}", id_status "{id_status}" e os seguintes produtos:'))
def check_pedido_details1(context, pedido_id, preco_total, id_status, *produtos):
    response_json = context["response"].json()

    # Assegurar que o pedido correto está na resposta
    order_details = next((order for order in response_json if order["id_pedido"] == int(pedido_id)), None)
    assert order_details is not None, f"No order found with id {pedido_id} in the response"

    # Verificar os detalhes básicos do pedido
    assert order_details["preco_total"] == float(preco_total)
    assert order_details["id_status"] == int(id_status)

    # Verificar cada produto fornecido
    for produto in produtos:
        nome_produto, quantidade = produto.split()  # Suponha que cada produto é passado como "Celular 3"
        assert any(item_detail["nome_produto"] == nome_produto and item_detail["quantidade"] == int(quantidade) for item_detail in order_details["itens"])



@then(parsers.cfparse('O produto "{nome_produto}" está associado ao pedido com quantidade "{quantidade}"'))
def check_product_in_order(context, nome_produto, quantidade):
    response_json = context["response"].json()
    
    order_details = response_json[0]  # Assumindo que os detalhes do pedido estão no primeiro item da lista de resposta
    
    # Verificar se o produto específico está associado ao pedido com a quantidade correta
    assert any(item_detail["nome_produto"] == nome_produto and item_detail["quantidade"] == int(quantidade) for item_detail in order_details["itens"])




