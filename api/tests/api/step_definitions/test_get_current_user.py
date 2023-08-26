# from pytest_bdd import parsers, given, when, then, scenario
# from api.tests.api.utils.f import get_token_test, get_user_test

# @scenario(scenario_name="Obter o usuário atual com um token válido", feature_name="../features/get_current_user.feature")
# def test_get_current_user():
#     """ Obter o usuário atual com um token válido """

# @given(parsers.cfparse('um usuário existente com email "{email}", senha "{senha}", nome "{nome}" e cpf "{cpf}" no banco de dados'))
# def mock_user(email: str, senha: str, nome: str, cpf: str):
#     """
#     Mock the get_user_test() method to return a user with the given email and password
#     """
#     user = get_user_test(email=email, cpf=cpf)
#     assert user is not None

# @given(parsers.cfparse('o usuário com email "{email}" e senha "{senha}" tem um token válido'))
# def mock_token(client, context, email: str, senha: str):
#     """
#     Mock the get_token_test() method to return a valid token
#     """
#     token = get_token_test(client, email, senha)
#     assert token is not None
#     context['token'] = token 
#     return context

# @when(
#     parsers.cfparse('uma requisição "GET" autenticada for enviada para "/usuario/me"'), 
#     target_fixture="context"
# )
# def send_request(client, context):
#     """
#     Send a GET request to "/usuario/me" with the valid token
#     """

#     response = client.get("/usuario/me", headers={"Authorization": f"Bearer {context['token']}"})
#     context["response"] = response
#     return context

# @then(parsers.cfparse('o status da resposta deve ser "{status_code:d}"'), target_fixture="context")
# def check_response_status_code(context, status_code: int):
#     """
#     Check if the response status code is the expected
#     """

#     assert context["response"].status_code == status_code
#     return context

# @then(
#     parsers.cfparse('o JSON da resposta deve conter o email "{email}", senha "HASH({password})", cpf "{cpf}" e nome "{name}"'), 
#     target_fixture="context"
# )
# def check_response_json_contains_user_data(context, email: str, password: str, cpf: str, name: str):
#     """
#     Check if the response JSON contains the expected user data
#     """

#     json_data = context["response"].json()
    
#     assert json_data["email"] == email
#     assert json_data["password"] == f"HASH({password})"
#     assert json_data["cpf"] == cpf
#     assert json_data["name"] == name
    
#     return context
