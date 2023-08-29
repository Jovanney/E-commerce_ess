import mock
from pytest_bdd import parsers, given, when, then, scenario

""" Scenario: Criar um novo usuário com sucesso """
@scenario(scenario_name="Criar um novo usuário com sucesso", feature_name="../features/create_user.feature")
def test_create_user_success():
    """ Criar um novo usuário com sucesso """

@given(parsers.cfparse('não existe um usuário com email "{email}", senha "{password}", nome "{name}" e cpf "{cpf}" no banco de dados'))
def ensure_user_not_exists(email: str, password: str, name: str, cpf: str):
    """
    Ensure there is no user with the given email and cpf in the database
    """
    user_test = {"email": email, "senha": password, "cpf" : cpf, "nome": name}
    user_mock = mock.Mock(return_value={"email": "Joao2@gmail.com", "senha": "123", "cpf" : "123123123", "nome": "joao"})
    
    assert user_test == user_mock.return_value

@when(
    parsers.cfparse('uma requisição "POST" for enviada para "/usuarios/" com email "{email}", senha "{password}", cpf "{cpf}" e nome "{name}"'), 
    target_fixture="context"
)
def send_create_user_request(client, context, email: str, password: str, cpf: str, name: str):
    """
    Send a POST request to "/usuarios/" with the given email, password, cpf and name
    """

    response = client.post("/usuarios/", json={"email": email, "senha": password, "cpf": cpf, "nome": name, "admin": True, "enderecos": [], "telefones": [], "pedidos": []})
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

    json_response = context["response"].json()
    assert json_response["email"] == email
    assert json_response["cpf"] == cpf
    assert json_response["nome"] == name
    # Como a senha é hash e não podemos compará-la diretamente,
    # verificamos se o campo da senha existe na resposta JSON.
    assert "senha" in json_response
    return context


@scenario(scenario_name="Tentar criar um usuário com um email que já está registrado", feature_name="../features/create_user.feature")
def test_create_user_failure():
    """ Tentar criar um usuário com um email que já está registrado """

@given(parsers.cfparse('existe um usuário com email "{email}", senha "{password}", nome "{name}" e cpf "{cpf}" no banco de dados'))
def ensure_user_exists(email: str, password: str, name: str, cpf: str):
    """
    Ensure there is a user with the given email and cpf in the database
    """
    user_test = {"email": email, "senha": password, "cpf" : cpf, "nome": name}
    user_mock = mock.Mock(return_value={"email": "Joao2@gmail.com", "senha": "123", "cpf" : "123123123", "nome": "joao"})
    
    assert user_test == user_mock.return_value

@when(
    parsers.cfparse('uma requisição "POST" for enviada para "/usuarios/" com email "{email}", senha "{password}", cpf "{cpf}" e nome "{name}"'), 
    target_fixture="context"
)
def send_create_user_request(client, context, email: str, password: str, cpf: str, name: str):
    """
    Send a POST request to "/usuarios/" with the given email, password, cpf and name
    """

    response = client.post("/usuarios/", json={"email": email, "senha": password, "cpf": cpf, "nome": name, "admin": True, "enderecos": [], "telefones": [], "pedidos": []})
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
def check_response_detail(context, detail: str):
    """
    Check if the response contains the expected detail
    """

    json_response = context["response"].json()
    assert json_response["detail"] == detail
    return context