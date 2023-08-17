from pytest_bdd import parsers, given, when, then, scenario
from api.tests.api.utils.utils import get_user_test

# Scenario: Tentar Exibir um Produto que está cadastrado no banco de dados
@scenario(feature_name="../features/features.feature", scenario_name="Tentar Exibir um Produto que está cadastrado no banco de dados")
def test_view_registered_product():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(cpf: str, email: str):
    pass  # Implement the necessary mock for a logged-in user

@given(parsers.cfparse('Quero Visualizar o produto com ID {product_id:d}'), target_fixture="context")
def mock_product_to_view(product_id: int):
    pass

@given(parsers.cfparse('Existe um produto com ID {product_id:d} na entidade Pedidos, com cnpj da loja "{cnpj}", categoria "{category}", nome "{name}", da marca "{brand}", Preço "{price}", e Especificações "{specifications}"'), target_fixture="context")
def mock_registered_product(context, product_id: int, cnpj: str, category: str, name: str, brand: str, price: str, specifications: str):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "product_id" in item
    assert item["product_id"] == product_id

    assert "cnpj" in item
    assert item["cnpj"] == cnpj
    
    assert "category" in item
    assert item["category"] == category
    assert "name" in item
    assert item["name"] == name
    assert "brand" in item
    assert item["brand"] == brand
    assert "price" in item
    assert item["price"] == price
    assert "specifications" in item
    assert item["specifications"] == specifications

    return context

@when(parsers.cfparse('Faço uma Requisição GET para a rota "{route}", Usando o ID do produto que quero consultar como parâmetro PATH'))
def send_get_product_request(client, context, route: str):
    """
    Send a GET request to the given route with the product ID as a path parameter
    """
    product_id = context["product_id"]
    response = client.get(f"{route}/{product_id}")
    context["response"] = response

@then(parsers.cfparse('É mostrado na tela todas as características(atributos) do produto com ID {product_id:d}'))
def check_product_attributes_displayed(context, product_id: int):

    response_data = context["response"].json()["data"]

    # Implement assertions to check if response data matches expected attributes
    assert response_data["id"] == str(product_id)
    assert "cnpj" in response_data
    assert "category" in response_data
    assert "name" in response_data
    assert "brand" in response_data
    assert "price" in response_data
    assert "specifications" in response_data

# ===================================================================================================================================

# Scenario: Tentar Exibir um Produto que não está cadastrado no banco de dados
@scenario(feature_name="../features/features.feature", scenario_name="Tentar Exibir um Produto que não está cadastrado no banco de dados")
def test_view_nonexistent_product():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(context, cpf: str, email: str):
    pass

@given(parsers.cfparse('Quero Visualizar o produto com ID {product_id:d}'))
def mock_product_to_view(product_id: int):
    pass

@given(parsers.cfparse('Não existe um produto com ID {product_id:d} na entidade Pedidos.'))
def mock_no_registered_product(product_id: int):
    pass  # Implement the necessary mock for no registered product

@when(parsers.cfparse('Faço uma Requisição GET para a rota "{route}", Usando o ID do produto que quero consultar como parâmetro PATH'))
def send_get_product_request(client, context, route: str):
    """
    Send a GET request to the given route with the product ID as a path parameter
    """

    product_id = context["product_id"]
    response = client.get(f"{route}/{product_id}")
    context["response"] = response

@then(parsers.cfparse('É retornado uma HTTPException informando que o produto não foi encontrado no banco de dados'))
def check_product_not_found_exception(context):
    """
    Check if a HTTPException indicating that the product was not found is returned
    """

    response = context["response"]
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "Produto não encontrado no banco de dados" in response.json()["detail"]

# ======================================================================================================

# Scenario: Adicionar um Produto ao menu geral com um ID ainda não utilizado
@scenario(feature_name="../features/features.feature", scenario_name="Adicionar um Produto ao menu geral com um ID ainda não utilizado")
def test_add_new_product_to_menu():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(cpf: str, email: str):
    pass  # Implement the necessary mock for a logged-in user

@given(parsers.cfparse('Quero adicionar o produto com ID {product_id:d}, com a loja de cnpj {cnpj}, com o nome igual a "{name}", da marca "{brand}", preço "{price}", e especificações "{specifications}"'))
def mock_product_to_add(product_id: int, cnpj: str, name: str, brand: str, price: str, specifications: str):
    pass  # Implement the necessary mock for the product to add

@given(parsers.cfparse('Não existe um produto com ID {product_id:d}'))
def mock_no_existing_product(product_id: int):
    pass  # Implement the necessary mock for no existing product

@given(parsers.cfparse('Existe uma loja com cnpj {cnpj}'))
def mock_existing_store(cnpj: str):
    pass  # Implement the necessary mock for an existing store

@when(parsers.cfparse('Faço uma Requisição POST para a rota "{route}", usando o ID do produto que quero inserir como parâmetro path'))
def send_post_product_request(client, context, route: str):
    """
    Send a POST request to the given route with the product ID as a path parameter
    """

    product_id = context["product_id"]
    request_data = {
        "cnpj": context["cnpj"],
        "name": context["name"],
        "brand": context["brand"],
        "price": context["price"],
        "specifications": context["specifications"]
    }
    response = client.post(f"{route}/{product_id}", json=request_data)
    context["response"] = response

@then(parsers.cfparse('O produto é adicionado a entidade “produto”'))
def check_product_added(context):
    """
    Check if the product is added to the entity "produto"
    """

    response = context["response"]
    assert response.status_code == 201

@then(parsers.cfparse('É retornado o produto criado'))
def check_created_product_returned(context):
    """
    Check if the created product is returned in the response
    """

    response_data = context["response"].json()["data"]

    # Implement assertions to check if response data matches expected attributes
    assert "id" in response_data
    assert "cnpj" in response_data
    assert "name" in response_data
    assert "brand" in response_data
    assert "price" in response_data
    assert "specifications" in response_data

# ==========================================================================================================================
# Scenario: Adicionar um Produto ao menu geral com um ID já utilizado
@scenario(feature_name="../features/features.feature", scenario_name="Adicionar um Produto ao menu geral com um ID já utilizado")
def test_add_product_with_existing_id():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(cpf: str, email: str):
    pass  # Implement the necessary mock for a logged-in user

@given(parsers.cfparse('Quero adicionar o produto com ID {product_id:d}, com a loja de cnpj {cnpj}, com o nome igual a "{name}", da marca "{brand}", preço "{price}", e especificações "{specifications}"'))
def mock_product_to_add(product_id: int, cnpj: str, name: str, brand: str, price: str, specifications: str):
    pass  # Implement the necessary mock for the product to add

@given(parsers.cfparse('Já existe um produto com ID {product_id:d}')) 
def mock_existing_product(context, product_id: int):
    response_data = context["response"].json()
    item = response_data["itens"][0]
    assert "product_id" in item
    assert item["product_id"] == product_id
    return context

@given(parsers.cfparse('Existe uma loja com cnpj {cnpj}'))
def mock_existing_store(cnpj: str):
    pass  # Implement the necessary mock for an existing store

@when(parsers.cfparse('Faço uma Requisição POST para a rota "{route}", usando o ID do produto que quero inserir como parâmetro path'))
def send_post_product_request(client, context, route: str):
    """
    Send a POST request to the given route with the product ID as a path parameter
    """

    product_id = context["product_id"]
    request_data = {
        "cnpj": context["cnpj"],
        "name": context["name"],
        "brand": context["brand"],
        "price": context["price"],
        "specifications": context["specifications"]
    }
    response = client.post(f"{route}/{product_id}", json=request_data)
    context["response"] = response

@then(parsers.cfparse('É retornado uma HTTPException informando que o ID já foi cadastrado'))
def check_duplicate_id_exception(context):
    """
    Check if a HTTPException is returned indicating that the ID is already registered
    """

    response = context["response"]
    assert response.status_code == 400

@then(parsers.cfparse('O produto não é adicionado ao banco de dados'))
def check_product_not_added(context):
    pass

# ===================================================================================================================
# Scenario: Tentar Excluir um produto que está cadastrado no banco de dados
@scenario(feature_name="../features/features.feature", scenario_name="Tentar Excluir um produto que está cadastrado no banco de dados")
def test_delete_registered_product():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(cpf: str, email: str):
    pass  # Implement the necessary mock for a logged-in user

@given(parsers.cfparse('Quero Excluir o Produto com ID {product_id:d}'))
def mock_product_to_delete(product_id: int):
    pass  # Implement the necessary mock for the product to delete

@given(parsers.cfparse('Existe um produto com ID {product_id:d} na entidade Pedidos, com cnpj da loja "{cnpj}", categoria "{category}", nome "{name}", da marca "{brand}", Preço "{price}", e Especificações "{specifications}"'))
def mock_registered_product(context, product_id: int, cnpj: str, category: str, name: str, brand: str, price: str, specifications: str):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "product_id" in item
    assert item["product_id"] == product_id

    assert "cnpj" in item
    assert item["cnpj"] == cnpj
    
    assert "category" in item
    assert item["category"] == category
    assert "name" in item
    assert item["name"] == name
    assert "brand" in item
    assert item["brand"] == brand
    assert "price" in item
    assert item["price"] == price
    assert "specifications" in item
    assert item["specifications"] == specifications

    return context

@when(parsers.cfparse('Faço uma requisição DELETE para a rota "{route}", Usando o ID do produto que quero Deletar como parâmetro PATH'))
def send_delete_product_request(client, context, route: str):
    """
    Send a DELETE request to the given route with the product ID as a path parameter
    """

    product_id = context["product_id"]
    response = client.delete(f"{route}/{product_id}")
    context["response"] = response

@then(parsers.cfparse('O Produto é apagado da entidade "{entity}" do banco de dados'))
def check_product_deleted(context, entity: str):
    """
    Check if the product is deleted from the specified entity in the database
    """
    pass

@then(parsers.cfparse('É retornada uma mensagem "{message}" para o usuário'))
def check_message_returned(context, message: str):
    """
    Check if the specified message is returned to the user
    """
    response = context["response"]
    assert response.status_code == 200  # Adjust the expected status code if needed
    assert response.json()["message"] == message

# ============================================================================
# Scenario: Tentar Excluir um produto que não está cadastrado no banco de dados
@scenario(feature_name="../features/features.feature", scenario_name="Tentar Excluir um produto que não está cadastrado no banco de dados")
def test_delete_nonexistent_product():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(cpf: str, email: str):
    pass  # Implement the necessary mock for a logged-in user

@given(parsers.cfparse('Quero Excluir o Produto com ID {product_id:d}'))
def mock_product_to_delete(product_id: int):
    pass  # Implement the necessary mock for the product to delete

@given(parsers.cfparse('Não Existe um produto com ID {product_id:d} na entidade Pedidos'))
def mock_nonexistent_product(product_id: int):
    pass  # Implement the necessary mock for a nonexistent product

@when(parsers.cfparse('Faço uma requisição DELETE para a rota "{route}", Usando o ID do produto que quero Deletar como parâmetro PATH'))
def send_delete_product_request(client, context, route: str):
    """
    Send a DELETE request to the given route with the product ID as a path parameter
    """

    product_id = context["product_id"]
    response = client.delete(f"{route}/{product_id}")
    context["response"] = response

@then(parsers.cfparse('É retornado uma HTTPException informando que o produto não foi encontrado na base de dados'))
def check_product_not_found(context):
    """
    Check if an HTTPException is returned indicating that the product was not found in the database
    """
    response = context["response"]
    # Implement necessary checks to ensure the correct HTTPException is returned
    pass

#==============================================================================================================
# Scenario: Tentar Atualizar um produto que está cadastrado no banco de dados
@scenario(feature_name="../features/features.feature", scenario_name="Tentar Atualizar um produto que está cadastrado no banco de dados")
def test_update_registered_product():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(cpf: str, email: str):
    pass  # Implement the necessary mock for a logged-in user

@given(parsers.cfparse('Quero atualizar o produto com ID {product_id:d}'))
def mock_product_to_update(product_id: int):
    pass  # Implement the necessary mock for the product to update

@given(parsers.cfparse('Existe um produto com ID {product_id:d} na entidade Pedidos, com cnpj da loja "{cnpj}", categoria "{category}", nome "{name}", da marca "{brand}", Preço "{price}", e Especificações "{specifications}"'))
def mock_registered_product(product_id: int, cnpj: str, category: str, name: str, brand: str, price: str, specifications: str):
    pass  # Implement the necessary mock for the registered product

@when(parsers.cfparse('Faço uma requisição PUT para a rota "{route}", Usando o ID do produto que quero Atualizar como parâmetro PATH e preencho os campos para ID {product_id:d}, CNPJ da loja "{new_cnpj}", categoria "{new_category}", nome "{new_name}", Marca "{new_brand}", preço "{new_price}", e Especificações "{new_specifications}"'))
def send_update_product_request(client, context, route: str, product_id: int, new_cnpj: str, new_category: str, new_name: str, new_brand: str, new_price: str, new_specifications: str):
    """
    Send a PUT request to the given route with the updated product attributes
    """

    # Implement the necessary request payload
    payload = {
        "id": product_id,
        "cnpj": new_cnpj,
        "category": new_category,
        "name": new_name,
        "brand": new_brand,
        "price": new_price,
        "specifications": new_specifications
    }

    response = client.put(f"{route}/{product_id}", json=payload)
    context["response"] = response

@then(parsers.cfparse('O pedido com ID {product_id:d} é atualizado na entidade “Produto” no banco de dados, sobrescrevendo os seus atributos para ID {product_id:d}, CNPJ da loja "{new_cnpj}", categoria "{new_category}", nome "{new_name}", Marca "{new_brand}", preço "{new_price}", e Especificações "{new_specifications}"'))
def check_product_updated(context, product_id: int, new_cnpj: str, new_category: str, new_name: str, new_brand: str, new_price: str, new_specifications: str):
    response_data = context["response"].json()

    item = response_data["itens"][0]
    assert "product_id" in item
    assert item["product_id"] == product_id
    assert "new_cnpj" in item
    assert item["new_cnpj"] == new_cnpj
    assert "new_category" in item
    assert item["new_category"] == new_category
    assert "new_name" in item
    assert item["new_name"] == new_name
    assert "new_brand" in item
    assert item["new_brand"] == new_brand
    assert "new_price" in item
    assert item["new_price"] == new_price
    assert "new_specifications" in item
    assert item["new_specifications"] == new_specifications

    return context

# =========================================================================================================
# Scenario: Tentar Atualizar um produto que não está cadastrado no banco de dados
@scenario(feature_name="../features/features.feature", scenario_name="Tentar Atualizar um produto que não está cadastrado no banco de dados")
def test_update_nonexistent_product():
    pass

# Step definitions for the new scenario
@given(parsers.cfparse('Sou um Usuário Logado no sistema com o cpf igual a "{cpf}" e email "{email}"'))
def mock_logged_in_user(cpf: str, email: str):
    pass  # Implement the necessary mock for a logged-in user

@given(parsers.cfparse('Quero atualizar o produto com ID {product_id:d}'))
def mock_product_to_update(product_id: int):
    pass  # Implement the necessary mock for the product to update

@given(parsers.cfparse('Não Existe um produto com ID {product_id:d} na entidade Pedidos'))
def mock_nonexistent_product(product_id: int):
    pass  # Implement the necessary mock for a non-existent product

@when(parsers.cfparse('Faço uma requisição PUT para a rota "{route}", Usando o ID do produto que quero Atualizar como parâmetro PATH e preencho os campos para ID {product_id:d}, CNPJ da loja "{new_cnpj}", categoria "{new_category}", nome "{new_name}", Marca "{new_brand}", preço "{new_price}", e Especificações "{new_specifications}"'))
def send_update_product_request(client, context, route: str, product_id: int, new_cnpj: str, new_category: str, new_name: str, new_brand: str, new_price: str, new_specifications: str):
  
    payload = {
        "id": product_id,
        "cnpj": new_cnpj,
        "category": new_category,
        "name": new_name,
        "brand": new_brand,
        "price": new_price,
        "specifications": new_specifications
    }

    response = client.put(f"{route}/{product_id}", json=payload)
    context["response"] = response

@then(parsers.cfparse('É retornado uma HTTPException informando que o produto não foi encontrado na base de dados'))
def check_product_not_found(context):
    """
    Check if a HTTPException is returned indicating that the product was not found in the database
    """
    response = context["response"]
    pass

