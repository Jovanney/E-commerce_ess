Feature: Usuários API

  Scenario: Atualizar a senha com sucesso
    Given um usuário existente com email "usuario@exemplo.com", senha "senha123", nome "Joao pedro" e cpf "123123123" no banco de dados
    And o usuário tem um token válido
    When uma requisição "PUT" autenticada for enviada para "/usuario/update_senha" com senha antiga "senha123" e nova senha "novaSenha123"
    Then o status da resposta deve ser "200"
    And a resposta deve conter o detalhe "Senha atualizada com sucesso"

  Scenario: Tentar atualizar a senha com uma senha antiga incorreta
    Given um usuário existente com email "usuario@exemplo.com", senha "senha123", nome "Joao pedro" e cpf "123123123" no banco de dados
    And o usuário tem um token válido
    When uma requisição "PUT" autenticada for enviada para "/usuario/update_senha" com senha antiga "senhaErrada" e nova senha "novaSenha123"
    Then o status da resposta deve ser "401"
    And a resposta deve conter o detalhe "Senha antiga incorreta"

  Scenario: Tentar atualizar a senha sem fornecer uma nova senha
    Given um usuário existente com email "usuario@exemplo.com", senha "senha123", nome "Joao pedro" e cpf "123123123" no banco de dados
    And o usuário tem um token válido
    When uma requisição "PUT" autenticada for enviada para "/usuario/update_senha" com senha antiga "senha123" e sem uma nova senha
    Then o status da resposta deve ser "400"
    And a resposta deve conter o detalhe "Nova senha não pode ser vazia"
