Feature: Create Loja API

  Scenario: Criar uma nova loja com sucesso
    Given não existe uma loja com email "loja@exemplo.com", senha "senha123", nome "Loja Exemplo" e cnpj "1231231230001" no banco de dados
    When uma requisição "POST" for enviada para "/loja/" com email "loja@exemplo.com", senha "senha123", cnpj "1231231230001" e nome "Loja Exemplo"
    Then o status da resposta deve ser "200"
    And o JSON da resposta deve conter o email "loja@exemplo.com", senha "HASH(senha123)", cnpj "1231231230001" e nome "Loja Exemplo"

  Scenario: Tentar criar uma loja com um email que já está registrado
    Given existe uma loja com email "loja@exemplo.com", senha "senha123", nome "Loja Exemplo" e cnpj "1231231230001" no banco de dados
    When uma requisição "POST" for enviada para "/loja/" com email "loja@exemplo.com", senha "senha123", cnpj "1231231230001" e nome "Loja Exemplo"
    Then o status da resposta deve ser "400"
    And a resposta deve conter o detalhe "Email already registered"
