Feature: Menu
  Scenario: Erro ao adicionar dois itens ao carrinho de lojas diferentes
    Given Estou na tela de Login
    And Eu preencho o campo Email com "daniel@gmail.com"
    And Eu preencho o campo Senha com "dadadada09"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Comprar" do produto "Camiseta"
    And Eu vejo o modal com a mensagem "Produto adicionado ao carrinho!"
    And Eu clico no botão "Comprar" do produto "rr"
    And Eu vejo o modal com a mensagem "Produto inserido não é da mesma loja que os produtos do carrinho!"