Feature: Usuários API

  Scenario: Obter o usuário atual com um token válido
    Given um usuário existente com email "Joao2@gmail.com", senha "123", nome "Joao pedro" e cpf "12312312312" no banco de dados
    And o usuário com email "Joao2@gmail.com" e senha "123" tem um token válido
    When uma requisição "GET" autenticada for enviada para "/usuario/me"
    Then o status da resposta deve ser "200"
    And o JSON da resposta deve conter o email "usuario@exemplo.com", senha "HASH(senha123)", cpf "12312312312" e nome "Joao pedro"

  Scenario: Tentar obter o usuário atual sem um token
    When uma requisição "GET" não autenticada for enviada para "/usuario/me"
    Then o status da resposta deve ser "401"
    And a resposta deve conter o detalhe "Invalid token"

  Scenario: Tentar obter o usuário atual com um token inválido
    When uma requisição "GET" autenticada com um token inválido for enviada para "/usuario/me"
    Then o status da resposta deve ser "401"
    And a resposta deve conter o detalhe "Invalid token"
