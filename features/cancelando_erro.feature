Feature: Historico3

  Scenario: Tentativa malsucedida de cancelamento de um pedido em rota
    Given Estou na tela de Login
    And Eu preencho o campo Email com "danielcursos09@gmail.com"
    And Eu preencho o campo Senha com "dadadada09"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Pedidos"
    And Eu sou redirecionado para essa página "http://localhost:3000/pedidos"
    And Eu vejo "ID Pedido: 10"
    And Eu vejo "Status: Em rota"
    And Eu clico no botão "Cancelar Pedido"
    And Eu vejo o modal com a mensagem "Erro ao cancelar pedido! Pedido já saiu para entrega. Não pode mais ser cancelado"