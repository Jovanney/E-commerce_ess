from pytest_bdd import parsers, given, when, then, scenario
from unittest.mock import Mock
from database.get_db import SessionLocal
from database.models.modelos import Usuario, Produto

""" Scenario: Exibir itens do carrinho"""
@scenario(scenario_name="Retornar itens de um pedido inexistente", feature_name="../features/carrinho.feature")
def test_exibir_itens():
    """ Exibir Carrinho"""

@given(parsers.cfparse('No banco de dados, não existe um pedido para o cpf "{cpf}"'))
def mock_no_order_in_db(cpf: str):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Usuario).filter(Usuario.cpf == cpf).first() is None
    db.close() 

@when(parsers.cfparse('Faço uma requisição GET para a rota "/pedidos/98765432111"'),
      target_fixture="context"
      )
def send_pedido_request(client, context):
    response = client.get("/pedidos/98765432111")
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser "{status_code:d}"'))
def check_response_status(context, status_code: int):
    assert context["response"].status_code == int(status_code)
    return context

@then(parsers.cfparse('a resposta deve conter o detalhe "{detail}"'))
def check_response_json_contains_product_data(context, detail):
    
    response_json = context["response"].json()

    assert "mensagem" in response_json and response_json["mensagem"] == detail
    return context

# # #================================================================================================================================================================================================

@scenario(scenario_name="Retornar itens de um pedido", feature_name="../features/carrinho.feature")
def test_itens_existentes():
    """ Exibir Carrinho"""

@given(parsers.cfparse('No banco de dados, existe um pedido para o cpf "{cpf}"')) 
def mock_cpf(cpf: str):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Usuario).filter(Usuario.cpf == cpf).first() is not None
    db.close()  

@when(parsers.cfparse('Faço uma requisição GET para a rota "/pedidos/98765432100"'),
      target_fixture="context"
      )
def send_request_pedid(client, context):
    response = client.get("/pedidos/98765432100")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor retorna id_pedido "{id_pedido}", quantidade "{quantidade}", id_produto "{id_produto}" e id_item "{id_item}"'))
def check_response(context, id_pedido, quantidade, id_produto, id_item):
    response_json = context["response"].json()

    assert response_json[0]["id_item"] == int(id_item)
    assert response_json[0]["id_pedido"] == int(id_pedido)
    assert response_json[0]["quantidade"] == int(quantidade)
    assert response_json[0]["id_produto"] == int(id_produto)


# # #================================================================================================================================================================================================

@scenario(scenario_name="Inserir um item ao carrinho de um cliente que ainda não tem um pedido", feature_name="../features/carrinho.feature")
def test_post_product():
    """ Exibir Carrinho"""

@given(parsers.cfparse('um produto existente no banco de dados com id_produto "{id_produto}"'))
def mock_product(id_produto):

    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is not None
    db.close()  

@when(parsers.cfparse('Faço uma requisição POST para a rota "/novo-item/" com id_produto "{id_produto}", usuario_cpf "{cpf}"  e quantidade "{quantidade}"'), target_fixture="context")
def send_post_pedido(client, context, id_produto: int, cpf: str, quantidade: int):

    response = client.post("/novo-item/", data = {"id_produto": id_produto, "usuario_cpf": cpf, "quantidade": quantidade})
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser "{status_code:d}"'))
def check_status(context, status_code: int):
    assert context["response"].status_code == status_code

@then(parsers.cfparse('é criado um pedido com id_item "{id_item}", e o produto com id "{id_produto}" foi adicionado ao meu carrinho com quantidade "{quantidade}".'))
def check_post_itens(context, id_item, id_produto, quantidade):
    return context

# #===============================================================================================    ===========================================================================

@scenario(scenario_name="Tentativa de inserção de um produto em um carrinho que não é da mesma loja que o produto que já está no carrinho", feature_name="../features/carrinho.feature")
def test_cart_ch():
    """exibir carrinho"""

@given(parsers.cfparse('No banco de dados, existe um item que tem um produto com id_produto "{id_produto}"'))
def mock_product_invalided(id_produto):

    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is not None
    db.close()  

@when(parsers.cfparse('Faço requisição POST para a rota "/novo-item/" com id_produto "{id_produto}", cpf "{cpf}" e a quantidade "{quantidade}"'))
def requisition_invalided(id_produto: int, cpf: str, quantidade: int, context, client):
    response = client.post("/novo-item/", data = {"id_produto": id_produto, "usuario_cpf": cpf, "quantidade": quantidade})
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser "{status_code:d}"'))
def check_status_invalided(context, status_code: int):
    assert context["response"].status_code == status_code
    
##################################################################################################################

@scenario(scenario_name="Remoção bem-sucedida de um item do carrinho", feature_name="../features/carrinho.feature")
def test_delete_item_for_pedido():
    pass

@given(parsers.cfparse('há um usuário existente no banco de dados com cpf "{cpf_user}", um pedido com status "{id_pedido}" e um produto com id "{id_produto}"'))
def set_parameters_service_response(context, cpf_user:str, id_pedido:str, id_produto:str) :
    context["cpf_user"] = cpf_user
    context["id_pedido"] = id_pedido
    context["id_produto"] = id_produto
    
@when(parsers.cfparse('faço uma requisição delete para a rota "{link}"'),
      target_fixture="context")
def send_test_delete_item_for_pedido(client, context, link:str):
    response = client.delete(link)
    context["response"] = response
    return context

@then(parsers.cfparse('recebo o status de resposta "{status_code}"'),
      target_fixture="context")
def check_response_status_code(context, status_code:int):
    assert str(context["response"].status_code ) == status_code
##################################################################################################################

@scenario(scenario_name="Limpeza bem-sucedida dos itens do carrinho", feature_name="../features/carrinho.feature")
def test_clear_cart():
    """teste_clear"""
    
@given(parsers.cfparse('há um usuário existente no banco de dados com cpf "{cpf_user}" onde há um pedido com status 1, contendo  um item'))
def set_parameters_clear_cart(context, cpf_user:str) :
    context["cpf_user"] = cpf_user

@when(parsers.cfparse('faço uma requisição delete para a rota "{link}"'),
      target_fixture="context")
def send_test_clear_cart(context, client, link:str):
    response = client.delete(link)
    context["response"] = response
    return context

@then(parsers.cfparse('recebo o status de resposta "{status_code}"'),
      target_fixture="context")
def check_response_status_code(context, status_code:str):
    assert str(context["response"].status_code) == status_code

##################################################################################################################

@scenario(scenario_name="atualizando o status do pedido do carrinho", feature_name="../features/carrinho.feature")
def test_update_status_pedido():
    """teste_update_status_pedido"""

@given(parsers.cfparse('há um usuário existente no banco de dados com cpf "{cpf_user}" onde há um pedido com status 1, contendo  um item'))
def set_parameters_update_status_pedido(context, cpf_user:str) :
    context["cpf_user"] = cpf_user

@when(parsers.cfparse('faço uma requisição patch para a rota "{link}"'),
      target_fixture="context")
def send_test_update_status_pedido(client, context, link:str):
    response = client.patch(link)
    context["status"] = response.json()
    context["response"] = response
    return context

@then(parsers.cfparse('recebo o status de resposta "{status_code}"'),
      target_fixture="context")
def check_response_status_code(context, status_code:str):
    assert str(context["response"].status_code) == status_code
    return context

@then(parsers.cfparse('recebo  status do pedido "{status}"'),
      target_fixture="context")
def check_response_new_status(context, status:int):
    assert context["status"][0] == int(status)
