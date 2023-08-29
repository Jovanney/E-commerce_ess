Feature: Usuários API

  Scenario: Obter o usuário atual com um token válido
    Given um usuário existente com email "Joao2@gmail.com", senha "123", nome "joao" e cpf "123123123" no banco de dados
    And o usuário com email "Joao2@gmail.com" e senha "123" tem um token válido
    When uma requisição "GET" autenticada for enviada para "/usuario/me"
    Then o status da resposta deve ser "200"
    And o JSON da resposta deve conter o email "Joao2@gmail.com", senha "HASH(senha123)", cpf "123123123" e nome "joao"

  Scenario: Tentar obter o usuário atual sem um token
    Given um usuário não existente no banco de dados
    When uma requisição "GET" não autenticada for enviada para "/usuario/me"
    Then o status da resposta deve ser "401"
    And a resposta deve conter o detalhe "Not authenticated"

  Scenario: Tentar obter o usuário atual com um token inválido
    Given um usuário existente com email "Joao2@gmail.com", senha "123", nome "joao" e cpf "123123123" no banco de dados
    When uma requisição "GET" autenticada com um token inválido for enviada para "/usuario/me"
    Then o status da resposta deve ser "401"
    And a resposta deve conter o detalhe "Could not validate credentials"
