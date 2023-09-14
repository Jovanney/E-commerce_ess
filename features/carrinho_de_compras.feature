Feature: cart
    Scenario: visualizando meus items no carrinho
    Given Estou na tela de Login
    And Eu preencho o campo Email com "carvalhodouglas95@gmail.com"
    And Eu preencho o campo Senha com "123123123"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Carrinho"
    And Eu sou redirecionado para essa página "http://localhost:3000/cart"

    Scenario: limpando o carrinho de compras
    Given Estou na tela de Login
    And Eu preencho o campo Email com "carvalhodouglas95@gmail.com"
    And Eu preencho o campo Senha com "123123123"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Carrinho"
    And Eu sou redirecionado para essa página "http://localhost:3000/cart"
    When Eu cliclo no botão "Limpar"