Feature: Create Usuario API

  Scenario: Criar um novo usuário com sucesso
    Given não existe um usuário com email "usuario@exemplo.com", senha "senha123", nome "Joao pedro" e cpf "123123123" no banco de dados
    When uma requisição "POST" for enviada para "/usuarios/" com email "usuario@exemplo.com", senha "senha123", cpf "123123123" e nome "Joao pedro"
    Then o status da resposta deve ser "200"
    And o JSON da resposta deve conter o email "usuario@exemplo.com", senha "HASH(senha123)", cpf "123123123" e nome "Joao pedro""

  Scenario: Tentar criar um usuário com um email que já está registrado
    Given existe um usuário com email "usuario@exemplo.com", senha "senha123", nome "Joao pedro" e cpf "123123123" no banco de dados
    When uma requisição "POST" for enviada para "/usuarios/" com email "usuario@exemplo.com", senha "senha123", cpf "123123123" e nome "Usuario"
    Then o status da resposta deve ser "400"
    And a resposta deve conter o detalhe "Email already registered"
