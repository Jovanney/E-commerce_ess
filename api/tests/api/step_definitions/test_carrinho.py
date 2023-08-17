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
@scenario(feature_name="../features/carrinho.feature", scenario_name="Removendo um item existente do carrinho")
def test_remove_item():
    pass

@given(parsers.cfparse('Sou um usuário registrado no sistema com CPF igual a "{cpf}"'))
def user_registered_with_cpf(cpf: str):
    pass

@given("Estou logado no sistema")
def user_logged_in():
    pass

@given(parsers.cfparse('No banco de dados, temos um pedido com ID {id_pedido:d}, cpf_usuario igual a "{cpf}" e preço igual a {preco:d}, com status = "{status}"'))
def order_exists_in_db(id_pedido: int, cpf: str, preco: int, status: str):
    pass

@given(parsers.cfparse('No carrinho, há um item com o produto com ID = {id_produto:d}, id_pedido = {id_pedido:d}, e quantidade = "{quantidade}"'))
def item_in_cart(id_produto: int, id_pedido: int, quantidade: str):
    pass

@when(parsers.cfparse('Faço uma requisição do tipo DELETE para a rota /remove-item/ informando id_produto = "{id_produto:d}", e o meu cpf'))
def send_remove_item_request(context, client, id_produto: int):
    response = client.delete(f"/remove-item/?id_produto={id_produto}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor processa minha requisição, atualizando a tabela Item, excluindo o item com ID = "{id_produto:d}", id_pedido = "{id_pedido:d}" e quantidade = "{quantidade}"'))
def check_item_removed(context, id_produto: int, id_pedido: int, quantidade: str):
    pass

#####################################################################################################################
@scenario('../features/carrinho.feature', 'Removendo um item inexistente do carrinho')
def test_remove_nonexistent_item():
    pass

@given(parsers.cfparse('Sou um usuário registrado no sistema com CPF igual a “{cpf}”'))
def mock_user_registered(cpf):
    pass

@given(parsers.cfparse('Estou logado no sistema'))
def mock_user_logged_in():
    pass

@given(parsers.cfparse('No banco de dados, temos um pedido com ID {id_pedido:d}, cpf_usuario igual a “{cpf}” e preço igual a {preco:f}, com status = "1"'))
def mock_existing_cart(cpf, id_pedido, preco):
    pass

@given(parsers.cfparse('No carrinho há apenas um item com o produto com ID = {id_produto:d}, id_pedido = {id_pedido:d}, e quantidade = “{quantidade}”'))
def mock_cart_with_item(id_produto, id_pedido, quantidade):
    pass

@when(parsers.cfparse('Faço uma requisição do tipo DELETE para a rota /remove-item/ informando o id_produto = "{id_produto}", e o meu cpf'))
def send_remove_item_request(client, id_produto, cpf):
    pass

@then(parsers.cfparse('O servidor processa minha requisição, retornando o erro "{error}"'))
def check_remove_item_response_error(error):
    pass

#####################################################################################################################
@scenario(feature_name="../features/carrinho.feature", scenario_name="Limpando todo o carrinho de uma vez com itens no carrinho")
def test_clear_cart_with_items():
    pass

@given(parsers.cfparse('Sou um usuário registrado no sistema com CPF igual a "{cpf}"'))
def user_registered_with_cpf(cpf: str):
    pass

@given("Estou logado no sistema")
def user_logged_in():
    pass

@given(parsers.cfparse('No banco de dados, temos um pedido com ID {id_pedido:d}, cpf_usuario igual a "{cpf}" e preço total igual a {preco_total:d}, com status = "{status}"'))
def order_exists_in_db(id_pedido: int, cpf: str, preco_total: int, status: str):
    pass

@given(parsers.cfparse('Nesse pedido, há dois itens, o primeiro com o produto ID = {produto_id_1:d}, id_pedido = {id_pedido:d}, e quantidade = "{quantidade_1}", e o segundo com o produto ID = {produto_id_2:d}, id_pedido = {id_pedido:d}, e quantidade = "{quantidade_2}"'))
def items_in_order(id_pedido: int, produto_id_1: int, quantidade_1: str, produto_id_2: int, quantidade_2: str):
    pass

@when(parsers.cfparse('Faço uma requisição do tipo DELETE para a rota /clear-carrinho/ informando o meu CPF'))
def send_clear_cart_request(context, client, cpf: str):
    response = client.delete(f"/clear-carrinho/?cpf={cpf}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor processa minha requisição, retornando a tabela Item, excluindo todos os itens do pedido relacionado ao meu CPF'))
def check_items_cleared(context):
    pass

@then("Exclui o pedido")
def check_order_deleted():
    pass

###################################################################################################################
@scenario('../features/carrinho.feature', 'Limpando o carrinho de uma vez com o carrinho já vazio')
def test_clear_empty_cart():
    pass

@given(parsers.cfparse('Sou um usuário registrado no sistema com CPF igual a “{cpf}”'))
def mock_user_registered(cpf):
    pass

@given(parsers.cfparse('Estou logado no sistema'))
def mock_user_logged_in():
    pass

@given(parsers.cfparse('No banco de dados, não temos nenhum pedido com status = ‘1’, não tem nada no carrinho'))
def mock_no_cart():
    pass

@when(parsers.cfparse('Faço uma requisição do tipo DELETE para a rota /clear-carrinho/ informando o meu CPF'), target_fixture="context")
def send_clear_cart_request(client, context, cpf):
    response = client.delete(f"/clear-carrinho/{cpf}")
    context["response"] = response
    return context

@then(parsers.cfparse('O servidor processa minha requisição, retornando o erro "{error}"'))
def check_clear_cart_response_error(error):
    pass
