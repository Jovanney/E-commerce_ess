from unittest.mock import Mock
from database.models.modelos import Usuario, Pedido

def get_user_test(cpf: str) -> Usuario:
    mock_user = Mock(spec=Usuario)
    mock_user.cpf = cpf
    mock_user.nome = "Mock User"
    mock_user.email = "mockuser@example.com"
    mock_user.senha = "mockpassword"
    mock_user.admin = False
    return mock_user

def get_pedido_by_id(pedido_id: int) -> Pedido:
    return None
