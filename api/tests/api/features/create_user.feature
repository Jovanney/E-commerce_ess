Feature: Create Usuario API

  Scenario: Criar um novo usuário com sucesso
    Given não existe um usuário com email "Joao2@gmail.com", senha "123", nome "joao" e cpf "123123123" no banco de dados
    When uma requisição "POST" for enviada para "/usuarios/" com email "Joao2@gmail.com", senha "123", cpf "123123123" e nome "joao"
    Then o status da resposta deve ser "200"
    And o JSON da resposta deve conter o email "Joao2@gmail.com", senha "HASH(senha123)", cpf "123123123" e nome "joao"

  Scenario: Tentar criar um usuário com um email que já está registrado
    Given existe um usuário com email "Joao2@gmail.com", senha "123", nome "joao" e cpf "123123123" no banco de dados
    When uma requisição "POST" for enviada para "/usuarios/" com email "Joao2@gmail.com", senha "123", cpf "123123123" e nome "Usuario"
    Then o status da resposta deve ser "400"
    And a resposta deve conter o detalhe "cpf already registered"
