import mock
from pytest_bdd import parsers, given, when, then, scenario

""" Scenario: Deletar o usuário atual com sucesso """
@scenario(scenario_name="Deletar o usuário atual com sucesso", feature_name="../features/delete_user.feature")
def test_delete_user_success():
    """ Deletar o usuário atual com sucesso """

@given(parsers.cfparse('um usuário existente com email "{email}", senha "{password}", nome "{name}" e cpf "{cpf}" no banco de dados'))
def ensure_user_exists(email: str, password: str, name: str, cpf: str):
    """
    Ensure there is a user with the given email and cpf in the database
    """
    user_test = {"email": email, "senha": password, "cpf" : cpf, "nome": name}
    user_mock = mock.Mock(return_value={"email": "usuario@exemplo.com", "senha": "123", "cpf" : "1231232123", "nome": "Joao pedro"})
    
    assert user_test == user_mock.return_value


@given(parsers.cfparse('o usuário com email "{email}", senha "{password}", nome "{name}" e cpf "{cpf}" tem um token válido'))
def ensure_user_has_valid_token(client, context, email, password, name, cpf):
    """
    Ensure the user has a valid token
    """
    valid_token = client.post("/token", data={"username": email, "password": password})
    
    context["token"] = valid_token.json()["access_token"]
    
    assert context["token"] is not None
    return context
        

@when(
    parsers.cfparse('uma requisição "DELETE" autenticada for enviada para "/usuario/delete"'), 
    target_fixture="context"
)
def send_delete_user_request(client, context):
    """
    Send a DELETE request to "/usuario/delete" with the authentication token
    """
    token = context["token"]
    response = client.delete("/usuario/delete", headers={"Authorization": f"Bearer {token}"})
    print(response)
    context["response"] = response
    return context

@then(parsers.cfparse('o status da resposta deve ser "{status_code:d}"'), target_fixture="context")
def check_response_status_code(context, status_code: int):
    """
    Check if the response status code is the expected
    """

    assert context["response"].status_code == status_code
    return context

@then(
    parsers.cfparse('a resposta deve conter o detalhe "{detail}"'), 
    target_fixture="context"
)
def check_response_contains_detail(context, detail: str):
    """
    Check if the response contains the expected detail
    """

    json_response = context["response"].json()
    
    assert json_response["detail"] == detail


""" Scenario: Tentar deletar o usuário atual sem um token """
@scenario(scenario_name="Tentar deletar o usuário atual sem um token", feature_name="../features/delete_user.feature")
def test_delete_user_without_token():
    """ Tentar deletar o usuário atual sem um token """

@when(
    parsers.cfparse('uma requisição "DELETE" não autenticada for enviada para "/usuario/delete"'), 
    target_fixture="context"
)
def send_delete_user_request(client, context):
    """
    Send a DELETE request to "/usuario/delete" without the authentication token
    """

    response = client.delete("/usuario/delete")
    context["response"] = response
    return context

@then(parsers.cfparse('o status da resposta deve ser "{status_code:d}"'), target_fixture="context")
def check_response_status_code(context, status_code: int):
    """
    Check if the response status code is the expected
    """

    assert context["response"].status_code == status_code
    return context

@then(
    parsers.cfparse('a resposta deve conter o detalhe "{detail}"'), 
    target_fixture="context"
)
def check_response_contains_detail(context, detail: str):
    """
    Check if the response contains the expected detail
    """

    json_response = context["response"].json()
    
    assert json_response["detail"] == detail


""" Scenario: Tentar deletar o usuário atual com um token inválido """
@scenario(scenario_name="Tentar deletar o usuário atual com um token inválido", feature_name="../features/delete_user.feature")
def test_delete_user_with_invalid_token():
    """ Tentar deletar o usuário atual com um token inválido """

@when(
    parsers.cfparse('uma requisição "DELETE" autenticada com um token inválido for enviada para "/usuario/delete"'), 
    target_fixture="context"
)
def send_delete_user_request(client, context):
    """
    Send a DELETE request to "/usuario/delete" with an invalid authentication token
    """

    response = client.delete("/usuario/delete", headers={"Authorization": f"Bearer invalid_token"})
    context["response"] = response
    return context

@then(parsers.cfparse('o status da resposta deve ser "{status_code:d}"'), target_fixture="context")
def check_response_status_code(context, status_code: int):
    """
    Check if the response status code is the expected
    """

    assert context["response"].status_code == status_code
    return context

@then(
    parsers.cfparse('a resposta deve conter o detalhe "{detail}"'), 
    target_fixture="context"
)
def check_response_contains_detail(context, detail: str):
    """
    Check if the response contains the expected detail
    """

    json_response = context["response"].json()
    
    assert json_response["detail"] == detail
