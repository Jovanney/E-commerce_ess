from pytest_bdd import parsers, given, when, then, scenario
from api.tests.api.utils.utils import get_user_test

#-------------------------------------------------------------------------------------------------------------------------
@scenario(feature_name="../features/carrinho.feature", scenario_name="Retornar itens de um pedido inexistente")
def test_cart_noexistent():
    pass

@given(parsers.cfparse('No banco de dados, não existe um pedido para o cpf "{cpf}"'))
def mock_no_order_in_db(cpf: str):
    pass

@when(parsers.cfparse('Faço uma requisição do tipo GET para a rota /pedidos/{cpf}'), target_fixture="context")
def send_pedido_request(client, context, cpf:str):
    response = client.get(f"/pedidos/{cpf}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor retorna um erro com detalhe "{detail}"'), target_fixture="context")
def check_response_detail(context, detail:str):
    assert "detail" in context["response"].json()
    assert context["response"].json()["detail"] == detail
    return context

# #--------------------------------------------------------------------------------------------------------------------------

@scenario(feature_name="../features/carrinho.feature", scenario_name="Retornar itens de um pedido")
def test_itens_retornar():
    pass

@given(parsers.cfparse('No banco de dados, existe um pedido para o cpf "{cpf}"'))
def mock_no_order_in_db(cpf: str):
    pass

@when(parsers.cfparse('Faço uma requisição do tipo GET para a rota /pedidos/{cpf}'), target_fixture="context")
def send_pedido_request(client, context, cpf:str):
    response = client.get(f"/pedidos/{cpf}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor retorna id_pedido "{id_pedido:d}", quantidade "{quantidade:d}", id_produto "{id_produto:d}" e id_item "{id_item:d}"'), target_fixture="context")
def check_response_items(context, id_pedido, quantidade, id_produto, id_item):
    response_data = context["response"].json()

    assert "id_pedido" in response_data
    assert response_data["id_pedido"] == id_pedido

    assert "itens" in response_data
    assert len(response_data["itens"]) == 1 

    item = response_data["itens"][0]
    assert "id_item" in item
    assert item["id_item"] == id_item

    assert "quantidade" in item
    assert item["quantidade"] == quantidade

    assert "id_produto" in item
    assert item["id_produto"] == id_produto

    return context

# #--------------------------------------------------------------------------------------------------------------------------
@scenario('../features/carrinho.feature', 'Inserir um item ao carrinho de um cliente que ainda não tem um pedido')
def test_insert_item_to_empty_cart():
    pass

@given(parsers.cfparse('Sou um Usuario registrado no sistema com o cpf igual a “{cpf}”'))
def mock_user_registered(cpf: str):
    pass
    

@given(parsers.cfparse('No banco de dados, temos um produto com id_produto igual a {id_produto:d}"'))
def mock_product_in_db(id_produto, context):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto
    return context

@when(parsers.cfparse('Faço uma requisição do tipo POST para a rota /novo-item/ informando o id_produto "{id_produto:d}", meu cpf e a quantidade {quantidade:d}'))
def send_add_item_request(context, id_produto, quantidade, cpf):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto

    assert "quantidade" in item
    assert item["quantidade"] == quantidade
    return context
    
@then(parsers.cfparse('Recebo uma mensagem informando que foi criado um pedido com id_item "{id_item:d}" e o produto com id "{id_produto:d}" foi adicionado ao meu carrinho com quantidade "{quantidade:d}" com sucesso.'))
def check_item_added_response(context, id_produto, quantidade, id_item):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto

    assert "quantidade" in item
    assert item["quantidade"] == quantidade

    assert "id_item" in item
    assert item["id_item"] == id_item
    return context

# #--------------------------------------------------------------------------------------------------------------------------
@scenario('../features/carrinho.feature', 'Tentativa de inserção de um produto em um carrinho que já possui um pedido no carrinho')
def test_insert_product_to_existing_cart():
    pass

@given(parsers.cfparse('Sou um Usuario registrado no sistema com o cpf igual a “{cpf}”'))
def mock_user_registered():
    pass

@given(parsers.cfparse('No banco de dados, temos um produto com id_produto igual a {id_produto:d}"'))
def mock_product_in_db(context,id_produto):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto
    return context

@given(parsers.cfparse('No banco de dados, temos um pedido com cpf_usuario igual a “{cpf}” e id_pedido = “{id_pedido:d}”'))
def mock_existing_cart(client, context, cpf, id_pedido):
    response = client.get(f"/pedidos/{cpf}")
    context["response"] = response

    response_data = context["response"].json()
    assert "id_pedido" in response_data
    assert response_data["id_pedido"] == id_pedido
    return context

@when(parsers.cfparse('Faço uma requisição do tipo POST para a rota /novo-item/ informando o id_produto "{id_produto:d}", meu cpf "{cpf}"e a quantidade {quantidade:d}'))
def send_add_item_request(context, client, id_produto, quantidade, cpf, id_item):
    response = client.get(f"/pedidos/{cpf}")
    context["response"] = response

    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto

    assert "quantidade" in item
    assert item["quantidade"] == quantidade

    assert "id_item" in item
    assert item["id_item"] == id_item
    return context
    
@then(parsers.cfparse('a função atualiza a quantidade do item que tem o produto com id = "{id_produto:d}"'))
def check_item_updated(context, id_produto):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto
    return context

# #----------------------------------------------------------------
@scenario('../features/carrinho.feature', 'Tentativa de inserção de um produto em um carrinho que não é da mesma loja que o produto que já está no carrinho')
def test_insert_product_different_store():
    pass

@given(parsers.cfparse('Sou um Usuario registrado no sistema com o cpf igual a "{cpf}"'))
def mock_user_registered(cpf):
    pass

@given(parsers.cfparse('No banco de dados, tenho um item que tem um produto com id_produto "{id_produto}" que é da loja com cnpj "{cnpj_loja}"'))
def mock_item_with_product(context, id_produto):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto
    return context



@when(parsers.cfparse('Faço requisição do tipo POST para a rota /novo-item/ informando o id_produto "{id_produto}", meu cpf "{cpf}" e a quantidade "{quantidade}"'))
def send_add_item_request(context, client, id_produto, cpf, quantidade):
    response = client.get(f"/pedidos/{cpf}")
    context["response"] = response

    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "id_produto" in item
    assert item["id_produto"] == id_produto

    assert "quantidade" in item
    assert item["quantidade"] == quantidade
    return context

@then(parsers.cfparse('O servidor retorna um erro com detalhe "{detail}"'))
def check_insert_product_different_store_response(context, detail: str):
    assert "detail" in context["response"].json()
    assert context["response"].json()["detail"] == detail
    return context