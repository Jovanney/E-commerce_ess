Feature: Gerenciamento de produtos

  Scenario: Indo para o gerenciamento de produtos
    Given Na tela de Login
    And Eu preencho o campo Email com "vitor.modesto.leitao@gmail.com"
    And Eu preencho o campo Senha com "Vitor_m26"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Produtos"
    And Eu clico no botão "Gerenciar Produto"
    And Eu sou redirecionado para essa página "http://localhost:3000/update"
    And Eu clico no botão "Alterar"
    And Eu preencho o campo Novo nome: com "Nome teste"
    And Eu clico em "Confirmar Atualização" 
    And Eu vejo o modal com a mensagem "Produto atualizado com sucesso"