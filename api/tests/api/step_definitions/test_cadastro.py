from pytest_bdd import parsers, given, when, then, scenario
from database.get_db import SessionLocal
from database.models.modelos import Produto
# ANTES DE RODAR: TEM QUE TER UM PRODUTO COM ID 4 E NAO PODE TER COM 3535
# Feito usando QUERY
""" Scenario: Tentar Exibir um Produto que não está cadastrado no banco de dados """
@scenario(scenario_name="Tentar Exibir um Produto que não está cadastrado no banco de dados", feature_name="../features/cadastro.feature")
def test_exibir_itens_fail():
    """ Exibir item """

@given(parsers.cfparse('um produto com id "{id_produto}" não está cadastrado no banco de dados'))
def auth_product_response_fail(id_produto):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is None
    db.close()  

@when(
    parsers.cfparse('Faço uma Requisição GET para a rota "/view_Produtos/2525"'), 
    target_fixture="context"
)
def send_product_request_fail(client, context):
    response = client.get("/view_Produtos/2525")
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser {status_code:d}'))
def check_response_status_code_product_fail(context, status_code: int):
    assert context["response"].status_code == status_code

@then(
     parsers.cfparse('a resposta deve conter o detalhe "Product not found"'), 
     target_fixture="context"
 )
def check_response_detail_fail(context):
    response_json = context["response"].json()
    assert "Product not found" == response_json["detail"]
    return context

# ==================================================================================

""" Scenario: Tentar Exibir um Produto que está cadastrado no banco de dados """
@scenario(scenario_name="Tentar Exibir um Produto que está cadastrado no banco de dados", feature_name="../features/cadastro.feature")
def test_exibir_itens_success():
    """ Exibir item """

@given(parsers.cfparse('um produto existente no banco de dados com id "{id_produto}"'))
def mock_auth_service_response_add_success(id_produto):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is not None
    db.close()  

@when(
    parsers.cfparse('Faço uma Requisição GET para a rota "/view_Produtos/2"'), 
    target_fixture="context"
)
def send_product_request_success(client, context):
    response = client.get("/view_Produtos/2")
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser {status_code:d}'))
def check_response_status_code_product_success(context, status_code: int):
    assert context["response"].status_code == status_code

@then(
    parsers.cfparse('a resposta JSON deve conter "2", "56789012345678", "Roupas", "Camiseta", "Marca B", "30" e "Cor Verde"')
)
def check_response_json_contains_product_success(context):
    response_json = context["response"].json()
    assert response_json["id_produto"] == 2
    assert response_json["cnpj_loja"] == "56789012345678"
    assert response_json["categoria_prod"] == "Roupas"
    assert response_json["nome_produto"] == "Camiseta"
    assert response_json["marca_produto"] == "Marca B"
    assert response_json["preco"] == '30'
    assert response_json["especificacoes"] == "Cor Verde"

# ====================================================================================
""" Scenario: Adicionar um Produto ao menu geral com um ID já utilizado """
@scenario(scenario_name="Adicionar um Produto ao menu geral com um ID já utilizado", feature_name="../features/cadastro.feature")
def test_add_product_fail():
    """ add bem-sucedido """

@given(parsers.cfparse('um produto existente no banco de dados com id "{id_produto}"'))
def mock_auth_service_response_add_fail(id_produto):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is not None
    db.close()  
    
@when(
    parsers.cfparse('uma Requisição é enviada para a rota /add_produtos/ com id "{id_produto}", com cnpj da loja "{cnpj_loja}", categoria "{categoria_prod}", nome "{nome_produto}", da marca "{marca_produto}", Preço "{preco}" e Especificações "{especificacoes}"'), 
    target_fixture="context"
)
def add_send_product_request_fail(client, context, id_produto, cnpj_loja, categoria_prod, nome_produto, marca_produto, preco, especificacoes):

    response = client.post("/add_produtos/", json={"id_produto": id_produto, "cnpj_loja": cnpj_loja,"categoria_prod":categoria_prod, "nome_produto":nome_produto, "marca_produto":marca_produto, "preco":preco, "especificacoes":especificacoes})
    context["response"] = response
    return context

@then(parsers.cfparse('o status da resposta deve ser {status_code}'), target_fixture="context")
def check_response_status_code_add_fail(context, status_code):
    assert context["response"].status_code == int(status_code)
    return context
@then(
    parsers.cfparse('a resposta deve conter o detalhe "{detail}"'),
    target_fixture="context"
)
def check_response_contains_detail_add_fail(context, detail: str):
    """
    Check if the response contains the specified detail
    """

    assert context["response"].json()["detail"] == detail
    return context

#=====================================================================================
""" Scenario: Adicionar um Produto ao menu geral com um ID ainda não utilizado """
@scenario(scenario_name="Adicionar um Produto ao menu geral com um ID ainda não utilizado", feature_name="../features/cadastro.feature")
def test_add_product_success():
    """ Exibir item """

@given(parsers.cfparse('um produto com id "{id_produto}" não está cadastrado no banco de dados'))
def mock_auth_service_response_add_success(id_produto):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is None
    db.close()  

@when(
    parsers.cfparse('uma Requisição é enviada para a rota /add_produtos/ com id "{id_produto}", com cnpj da loja "{cnpj_loja}", categoria "{categoria_prod}", nome "{nome_produto}", da marca "{marca_produto}", Preço "{preco}" e Especificações "{especificacoes}"'), 
    target_fixture="context"
)
def send_add_request_success(client, context, id_produto, cnpj_loja, categoria_prod, nome_produto, marca_produto, preco, especificacoes):

    response = client.post("/add_produtos/", json={"id_produto": id_produto, "cnpj_loja": cnpj_loja,"categoria_prod":categoria_prod, "nome_produto":nome_produto, "marca_produto":marca_produto, "preco":preco, "especificacoes":especificacoes})
    context["response"] = response
    return context

@then(parsers.cfparse('o status da resposta deve ser {status_code}'), target_fixture="context")
def check_response_status_code_add_success(context, status_code):
    assert context["response"].status_code == int(status_code)
    return context

@then(
    parsers.cfparse('A resposta JSON Deve conter "3535", "56789012345678", "Roupas", "Meia", "adidas", "23" e "35-42"')
)
def check_response_json_contains_product_data_add_success(context):
    response_json = context["response"].json()
    assert response_json["id_produto"] == 3535
    assert response_json["cnpj_loja"] == "56789012345678"
    assert response_json["categoria_prod"] == "Roupas"
    assert response_json["nome_produto"] == "Meia"
    assert response_json["marca_produto"] == "adidas"
    assert response_json["preco"] == '23'
    assert response_json["especificacoes"] == "35-42"

# ===================================================================================
# Feito usando QUERY
""" Scenario: Tentar Atualizar um produto que está cadastrado no banco de dados """
@scenario(scenario_name="Tentar Atualizar um produto que está cadastrado no banco de dados", feature_name="../features/cadastro.feature")
def test_update_success():
    """ Atualização bem-sucedida """

@given(parsers.cfparse('um produto existente no banco de dados com id "{id_produto}"'))
def mock_auth_service_update_response_success(id_produto):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is not None
    db.close()  
    
@when(
    parsers.cfparse('uma requisição PUT é enviada para a rota "/update_produto/{id_produto}", com ID "{id_produto}",CNPJ da loja "{cnpj_loja}", categoria "{categoria_prod}", nome "{nome_produto}", Marca "{marca_produto}", preço "{preco}" e Especificações "{especificacoes}"'), 
    target_fixture="context"
)
def send_update_request_success(client, context, categoria_prod, nome_produto, marca_produto, preco, especificacoes):

    response = client.put(f"/update_produto/1?new_categoria={categoria_prod}&new_nome={nome_produto}&new_marca={marca_produto}&new_preco={preco}&new_especificacoes={especificacoes}")

    context["response"] = response
    return context


@then(parsers.cfparse('o status da resposta deve ser {status_code:d}'), target_fixture="context")
def check_response_update_code_success(context, status_code: int):
    assert context["response"].status_code == status_code
    return context

@then(
    parsers.cfparse('A resposta JSON Deve conter "1", "12345678901234", "Eletrônico", "Monitor XGB", "LG", "1000" e "16 polegadas"'), 
    target_fixture="context"
)
def check_response_json_contains_update_data_success(context):
    response_json = context["response"].json()
    assert response_json["id_produto"] == 1
    assert response_json["cnpj_loja"] == "12345678901234"
    assert response_json["categoria_prod"] ==  "Eletrônico"
    assert response_json["nome_produto"] == "Monitor XGB"
    assert response_json["marca_produto"] == "LG"
    assert response_json["preco"] == '1000' 
    assert response_json["especificacoes"] == "16 polegadas"

# =========================================================================
# Feito usando QUERY
""" Scenario: Tentar Atualizar um produto que não está cadastrado no banco de dados """
@scenario(scenario_name="Tentar Atualizar um produto que não está cadastrado no banco de dados", feature_name="../features/cadastro.feature")
def test_update_itens_fail():
    """ Exibir item """

@given(parsers.cfparse('um produto com id "{id_produto}" não está cadastrado no banco de dados'))
def mock_auth_service_response_update_fail(id_produto):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is None
    db.close()  

@when(
    parsers.cfparse('uma requisição PUT é enviada para a rota "/update_produto/2525", com ID "{id_produto}", categoria "{categoria_prod}", nome "{nome_produto}", Marca "{marca_produto}", preço "{preco}" e Especificações "{especificacoes}"'), 
    target_fixture="context"
)
def send_update_request_fail(client, context, categoria_prod, nome_produto, marca_produto, preco, especificacoes):

    response = client.put(f"/update_produto/2525?new_categoria={categoria_prod}&new_nome={nome_produto}&new_marca={marca_produto}&new_preco={preco}&new_especificacoes={especificacoes}")

    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser {status_code:d}'))
def check_response_status_code_product_update_fail(context, status_code: int):
    assert context["response"].status_code == status_code

@then(
     parsers.cfparse('a resposta deve conter o detalhe "Product not found"'), 
     target_fixture="context"
 )
def check_response_detail_update_fail(context):
    response_json = context["response"].json()
    assert "Product not found" == response_json["detail"]
    return context

# =====================================================================

# Feito usando QUERY
"""
Antes de rodar tem que adiconar o produto com id 4 no banco de dados
{
  "id_produto": 4,
  "cnpj_loja": "56789012345678",
  "categoria_prod": "Roupas",
  "nome_produto": "casaco",
  "marca_produto": "Renner",
  "preco": "150",
  "especificacoes": "Cor azul",
  "itens": []
}
"""
""" Scenario: Tentar Excluir um produto que está cadastrado no banco de dados"""
@scenario(scenario_name="Tentar Excluir um produto que está cadastrado no banco de dados", feature_name="../features/cadastro.feature")
def test_del_itens_success():
    """ Exibir item """

@given(parsers.cfparse('um produto existente no banco de dados com id "{id_produto}"'))
def mock_auth_service_response_del_success(id_produto):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is not None
    db.close()  

@when(
    parsers.cfparse('uma requisição é enviada para a rota "/del_produtos/4"'), 
    target_fixture="context"
)
def send_product_request_del_success(client, context):
    response = client.delete("/del_produtos/4")
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser {status_code:d}'))
def check_response_status_code_product_del_success(context, status_code: int):
    assert context["response"].status_code == status_code
    return context

@then(
    parsers.cfparse('A resposta JSON Deve conter "Product Deleted"')
)
def check_response_json_contains_product_data_del_success(context):
    response_json = context["response"].json()
    assert "Product Deleted" == response_json["message"]


#=================================================================

# Feito usando QUERY
""" Scenario: Tentar Excluir um produto que não está cadastrado no banco de dados"""
@scenario(scenario_name="Tentar Excluir um produto que não está cadastrado no banco de dados", feature_name="../features/cadastro.feature")
def test_del_itens_fail():
    """ Exibir item """

@given(parsers.cfparse('Um produto com id "{id_produto}" não está cadastrado no banco de dados'))
def mock_auth_service_response_del_fail(id_produto):

    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == id_produto).first() is None
    db.close()  

@when(
     parsers.cfparse('uma requisição é enviada para a rota "/del_produtos/40"'), 
     target_fixture="context"
 )
def send_product_request_del_fail(client, context):
    response = client.delete("/del_produtos/40")
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser {status_code:d}'), target_fixture="context")
def check_response_status_code_del_fail(context, status_code: int):
    assert context["response"].status_code == status_code
    return context

@then(
     parsers.cfparse('a resposta deve conter o detalhe "Product not found"'), 
     target_fixture="context"
 )
def check_response_detail_del_fail(context):
    response_json = context["response"].json()
    assert "Product not found" == response_json["detail"]
    return context

# ================================================================================
""" Scenario: Exibir todos os produtos do banco de dados """
@scenario(scenario_name="Exibir todos os produtos do banco de dados", feature_name="../features/cadastro.feature")
def test_exibir_all_itens():
    """ Exibir item """

@given(parsers.cfparse('produtos existentes no banco de dados com id "{produto_1}", "{produto_2}", "{produto_3}"'))
def auth_product_response_fail(produto_1, produto_2, produto_3):
    db = SessionLocal()  # Use SessionLocal para obter uma sessão do banco de dados
    assert db.query(Produto).filter(Produto.id_produto == produto_1).first() is not None
    assert db.query(Produto).filter(Produto.id_produto == produto_2).first() is not None
    assert db.query(Produto).filter(Produto.id_produto == produto_3).first() is not None
    db.close()  

@when(
    parsers.cfparse('Faço uma Requisição GET para a rota "/All_Produtos/"'), 
    target_fixture="context"
)
def send_product_request_fail(client, context):
    response = client.get("/All_Produtos/")
    context["response"] = response
    return context

@then(parsers.cfparse('O status da resposta deve ser {status_code:d}'))
def check_response_status_code_product_fail(context, status_code: int):
    assert context["response"].status_code == status_code

@then(
    parsers.cfparse('a resposta JSON deve conter "1", "12345678901234", "Eletrônico", "Monitor XGB", "LG", "1000" e "16 polegadas", "2", "56789012345678", "Roupas", "Camiseta", "Marca B", "30" e "Cor Verde", "3", "56789012345678", "esportes", "bola futebol", "adidas", "50" e "..."')
)
def check_response_json_contains_all_products(context):
    response_json = context["response"].json()
    expected_products = [
        {
            "id_produto": 1,
            "cnpj_loja": "12345678901234",
            "categoria_prod": "Eletrônico",
            "nome_produto": "Monitor XGB",
            "marca_produto": "LG",
            "especificacoes": "16 polegadas",
            "preco": "1000"
        },
        {
            "id_produto": 2,
            "cnpj_loja": "56789012345678",
            "categoria_prod": "Roupas",
            "nome_produto": "Camiseta",
            "marca_produto": "Marca B",
            "especificacoes": "Cor Verde",
            "preco": "30"
        },
        {
            "id_produto": 3,
            "cnpj_loja": "56789012345678",
            "categoria_prod": "esportes",
            "nome_produto": "bola futebol",
            "marca_produto": "adidas",
            "especificacoes": "...",
            "preco": "50"
        }
    ]
    for expected_product in expected_products:
        assert expected_product in response_json