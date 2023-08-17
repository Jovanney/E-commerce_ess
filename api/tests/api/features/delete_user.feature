Feature: Usuários API

  Scenario: Deletar o usuário atual com sucesso
    Given um usuário existente com email "usuario@exemplo.com", senha "senha123", nome "Joao pedro" e cpf "123123123" no banco de dados
    And o usuário tem um token válido
    When uma requisição "DELETE" autenticada for enviada para "/usuario/delete"
    Then o status da resposta deve ser "200"
    And a resposta deve conter o detalhe "Usuário deletado com sucesso"

  Scenario: Tentar deletar o usuário atual sem um token
    When uma requisição "DELETE" não autenticada for enviada para "/usuario/delete"
    Then o status da resposta deve ser "401"
    And a resposta deve conter o detalhe "Invalid token"

  Scenario: Tentar deletar o usuário atual com um token inválido
    When uma requisição "DELETE" autenticada com um token inválido for enviada para "/usuario/delete"
    Then o status da resposta deve ser "401"
    And a resposta deve conter o detalhe "Invalid token"
