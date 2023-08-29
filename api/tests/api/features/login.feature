Feature: Login API

    Scenario: Login bem-sucedido
        Given um usuário existente no banco de dados com email "Joao2@gmail.com", senha "123", cpf "12312312312" e nome "Joao"
        When uma requisição POST é enviada para "/token" com email "Joao2@gmail.com" e senha "123"
        Then o status da resposta deve ser 200
        And a resposta JSON deve conter "access_token" e "token_type"

    Scenario: Falha no login devido a credenciais não existentes no banco
        Given um usuário com email "usuario@teste.com", senha "senha123", cpf = "00000000000" e nome = "carlos" não está cadastrado no banco
        When uma requisição POST é enviada para "/token" com email "usuario@teste.com" e senha "senha123"
        Then o status da resposta deve ser 401
        And a resposta deve conter o detalhe "Incorrect username or password"

    Scenario: Falha no login devido a email incorreto
        Given um usuário existente no banco de dados com email "Joao2@gmail.com", senha "123", cpf "12312312312" e nome "Joao"
        When uma requisição POST é enviada para "/token" com email "email_errado@teste.com" e senha "123"
        Then o status da resposta deve ser "401"
        And a resposta deve conter o detalhe "Incorrect username or password"

    Scenario: Falha no login devido a senha incorreta
        Given um usuário existente no banco de dados com email "Joao2@gmail.com", senha "123", cpf "12312312312" e nome "Joao"
        When uma requisição POST é enviada para "/token" com email "Joao2@gmail.com" e senha "senha_incorreta"
        Then o status da resposta deve ser "401"
        And a resposta deve conter o detalhe "Incorrect username or password"
