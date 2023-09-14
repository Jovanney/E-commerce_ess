Feature: Historico

  Scenario: Indo para o historico de Pedidos
    Given Estou na tela de Login
    And Eu preencho o campo Email com "danielreinaux00@gmail.com"
    And Eu preencho o campo Senha com "dadadada09"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Pedidos"
    And Eu sou redirecionado para essa página "http://localhost:3000/pedidos"
    And Eu vejo "ID Pedido: 6"
    And Eu vejo "Preço Total: R$ 149.95"
    And Eu vejo "Status: Confirmado"
    And Eu vejo "Itens do Pedido:"
    And Eu vejo "5x Camiseta"