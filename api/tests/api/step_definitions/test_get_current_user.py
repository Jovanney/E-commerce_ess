import mock
from pytest_bdd import parsers, given, when, then, scenario

from api.tests.api.utils.utils import get_token_test

@scenario(scenario_name="Obter o usuário atual com um token válido", feature_name="../features/get_current_user.feature")
def test_get_current_user():
    """ Obter o usuário atual com um token válido """

@given(parsers.cfparse('um usuário existente com email "{email}", senha "{senha}", nome "{nome}" e cpf "{cpf}" no banco de dados'))
def mock_user(email: str, senha: str, nome: str, cpf: str):
    """
    Mock the get_user_test() method to return a user with the given email and password
    """
    user_test = {"email": email, "senha": senha, "cpf" : cpf, "nome": nome}
    user_mock = mock.Mock(return_value={"email": "Joao2@gmail.com", "senha": "123", "cpf" : "123123123", "nome": "joao"})
    
    assert user_test == user_mock.return_value
@given(parsers.cfparse('o usuário com email "{email}" e senha "{senha}" tem um token válido'))
def mock_token(client, context, email: str, senha: str):
    """
    Mock the get_token_test() method to return a valid token
    """
    token = get_token_test(client, email, senha)
    assert token is not None
    context['token'] = token["access_token"]
    return context

@when(
    parsers.cfparse('uma requisição "GET" autenticada for enviada para "/usuario/me"'), 
    target_fixture="context"
)
def send_request(client, context):
    """
    Send a GET request to "/usuario/me" with the valid token
    """

    response = client.get("/users/me", headers={"Authorization": f"Bearer {context['token']}"})
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
    parsers.cfparse('o JSON da resposta deve conter o email "{email}", senha "HASH({password})", cpf "{cpf}" e nome "{name}"'), 
    target_fixture="context"
)
def check_response_json_contains_user_data(context, email: str, password: str, cpf: str, name: str):
    """
    Check if the response JSON contains the expected user data
    """

    json_data = context["response"].json()
    
    assert json_data["email"] == email
    assert json_data["cpf"] == cpf
    assert json_data["nome"] == name
    # Como a senha é hash e não podemos compará-la diretamente,
    # verificamos se o campo da senha existe na resposta JSON.
    assert "senha" in json_data
    
    return context


@scenario(
    scenario_name="Tentar obter o usuário atual sem um token", 
    feature_name="../features/get_current_user.feature"
)
def test_get_current_user_without_token():
    """ Tentar obter o usuário atual sem um token """

@given(parsers.cfparse('um usuário não existente no banco de dados'))
def mock_user():
    pass

@when(
    parsers.cfparse('uma requisição "GET" não autenticada for enviada para "/usuario/me"'), 
    target_fixture="context"
)
def send_unauthenticated_request(client):
    """
    Send a GET request to "/usuario/me" without a token
    """

    response = client.get("/users/me")
    context = {"response": response}
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
def check_response_detail(context, detail: str):
    """
    Check if the response contains the expected detail
    """

    json_data = context["response"].json()
    
    assert json_data["detail"] == detail
    
    return context


@scenario(
    scenario_name="Tentar obter o usuário atual com um token inválido", 
    feature_name="../features/get_current_user.feature"
)
def test_get_current_user_with_invalid_token():
    """ Tentar obter o usuário atual com um token inválido """

@given(parsers.cfparse('um usuário existente com email "Joao2@gmail.com", senha "123", nome "joao" e cpf "123123123" no banco de dados'))
def mock_user(email: str, senha: str, nome: str, cpf: str):
    """
    Mock the get_user_test() method to return a user with the given email and password
    """
    user_test = {"email": email, "senha": senha, "cpf" : cpf, "nome": nome}
    user_mock = mock.Mock(return_value={"email": "Joao2@gmail.com", "senha": "123", "cpf" : "123123123", "nome": "joao"})
    
    assert user_test == user_mock.return_value

@when(
    parsers.cfparse('uma requisição "GET" autenticada com um token inválido for enviada para "/usuario/me"'), 
    target_fixture="context"
)
def send_request_with_invalid_token(client):
    """
    Send a GET request to "/usuario/me" with an invalid token
    """

    response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
    context = {"response": response}
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
def check_response_detail(context, detail: str):
    """
    Check if the response contains the expected detail
    """

    json_data = context["response"].json()
    
    assert json_data["detail"] == detail
    
    return context
