from unittest.mock import Mock
from database.models.modelos import Usuario, Pedido

def get_user_test(cpf: str) -> Usuario:

    """
    This function simulates fetching a user from the database by a given CPF.
    Here, we return a mock user for testing purposes.
    """
    mock_user = Mock(spec=Usuario)
    mock_user.cpf = cpf
    mock_user.nome = "Mock User"
    mock_user.email = "mockuser@example.com"
    mock_user.senha = "mockpassword"
    mock_user.admin = False
    return mock_user

def get_pedido_by_id(pedido_id: int) -> Pedido:
    return None

    """
    This function simulates fetching an order by its ID from the database.
    Here, we return None to simulate the absence of the order for testing purposes.
    """
    return None

def get_token_test(client, email, senha):
    responde = client.post("/token", data={"username": email, "password": senha})
    return responde.json()