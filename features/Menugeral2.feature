Feature: Menu
  Scenario: Adicionando um item ao carrinho na tela do Menu Geral
    Given Estou na tela de Login
    And Eu preencho o campo Email com "daniel@gmail.com"
    And Eu preencho o campo Senha com "dadadada09"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Comprar"
    And Eu vejo o modal com a mensagem "Produto adicionado ao carrinho!"