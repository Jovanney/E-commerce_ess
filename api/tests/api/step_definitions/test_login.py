from pytest_bdd import parsers, given, when, then, scenario
import mock


""" Scenario: Login bem-sucedido """
@scenario(scenario_name="Login bem-sucedido", feature_name="../features/login.feature")
def test_login_success():
    """ Login bem-sucedido """

@given(parsers.cfparse('um usuário existente no banco de dados com email "{email}", senha "{password}", cpf "{cpf}" e nome "{name}"'))
def mock_auth_service_response(email: str, password: str, cpf: str, name: str):
    """
    Mock the  return a user with the given email and password
    """
    user_test = {"email": email, "senha": password, "cpf" : cpf, "nome": name}
    user_mock = mock.Mock(return_value={"email": "Joao2@gmail.com", "senha": "123", "cpf" : "12312312312", "nome": "Joao"})
    
    assert user_test == user_mock.return_value
    
@when(
    parsers.cfparse('uma requisição POST é enviada para "/token" com email "{email}" e senha "{password}"'), 
    target_fixture="context"
)
def send_login_request(client, context, email: str, password: str):
    """
    Send a POST request to "/token" with the given email and password
    """

    response = client.post("/token", data={"username": email, "password": password})
    context["response"] = response
    return context

@then(parsers.cfparse('o status da resposta deve ser {status_code:d}'), target_fixture="context")
def check_response_status_code(context, status_code: int):
    """
    Check if the response status code is the expected
    """

    assert context["response"].status_code == status_code
    return context

@then(
    parsers.cfparse('a resposta JSON deve conter "access_token" e "token_type"'), 
    target_fixture="context"
)
def check_response_json_contains_token_data(context):
    """
    Check if the response JSON contains "access_token" and "token_type"
    """

    assert "access_token" in context["response"].json()
    assert "token_type" in context["response"].json()
    return context


""" Scenario: Falha no login devido a credenciais não existentes no banco """
@scenario(scenario_name="Falha no login devido a credenciais não existentes no banco", feature_name="../features/login.feature")
def test_login_failure():
    """ Falha no login devido a credenciais não existentes no banco """

@given(parsers.cfparse('um usuário com email "{email}", senha "{password}", cpf = "{cpf}" e nome = "{name}" não está cadastrado no banco'))
def ensure_user_not_exists(email: str, password: str, cpf: str, name: str):
    """
    Ensure there is no user with the given email and cpf in the database
    """
    user_test = {"email": email, "senha": password, "cpf" : cpf, "nome": name}
    user_mock = mock.Mock(return_value=None)

    assert user_test != user_mock.return_value

@when(
    parsers.cfparse('uma requisição POST é enviada para "/token" com email "{email}" e senha "{password}"'), 
    target_fixture="context"
)
def send_login_request(client, context, email: str, password: str):
    """
    Send a POST request to "/token" with the given email and password
    """

    response = client.post("/token", data={"username": email, "password": password})
    context["response"] = response
    return context

@then(parsers.cfparse('o status da resposta deve ser {status_code:d}'), target_fixture="context")
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

    assert context["response"].json()["detail"] == detail
    print(context)
    return context


""" Scenario: Falha no login devido a email incorreto """
@scenario(scenario_name="Falha no login devido a email incorreto", feature_name="../features/login.feature")
def test_login_failure_due_to_incorrect_email():
    """ Falha no login devido a email incorreto """

@given(parsers.cfparse('um usuário existente no banco de dados com email "{email}", senha "{password}", cpf "{cpf}" e nome "{name}"'))
def create_user_in_database(email: str, password: str, cpf: str, name: str):
    """
    Ensure there is the user with the given email and cpf in the database
    """
    user_test = {"email": email, "senha": password, "cpf" : cpf, "nome": name}
    user_mock = mock.Mock(return_value={"email": "Joao2@gmail.com", "senha": "123", "cpf" : "12312312312", "nome": "Joao"})
    
    assert user_test == user_mock.return_value

@when(
    parsers.cfparse('uma requisição POST é enviada para "/token" com email "{email}" e senha "{password}"'), 
    target_fixture="context"
)
def send_login_request(client, context, email: str, password: str):
    """
    Send a POST request to "/token" with the given email and password
    """

    response = client.post("/token", data={"username": email, "password": password})
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

    assert context["response"].json()["detail"] == detail
    return context


""" Scenario: Falha no login devido a senha incorreta """
@scenario(scenario_name="Falha no login devido a senha incorreta", feature_name="../features/login.feature")
def test_login_failure_due_to_incorrect_password():
    """ Falha no login devido a senha incorreta """

@given(parsers.cfparse('um usuário existente no banco de dados com email "{email}", senha "{password}", cpf "{cpf}" e nome "{name}"'))
def create_user_in_database(email: str, password: str, cpf: str, name: str):
    """
    Ensure there is the user with the given email and cpf in the database
    """
    user_test = {"email": email, "senha": password, "cpf" : cpf, "nome": name}
    user_mock = mock.Mock(return_value={"email": "Joao2@gmail.com", "senha": "123", "cpf" : "12312312312", "nome": "Joao"})
    
    assert user_test == user_mock.return_value

@when(
    parsers.cfparse('uma requisição POST é enviada para "/token" com email "{email}" e senha "{password}"'), 
    target_fixture="context"
)
def send_login_request(client, context, email: str, password: str):
    """
    Send a POST request to "/token" with the given email and password
    """

    response = client.post("/token", data={"username": email, "password": password})
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

    assert context["response"].json()["detail"] == detail
    return context
