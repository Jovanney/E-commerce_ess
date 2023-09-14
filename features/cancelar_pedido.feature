Feature: Historico2 

  Scenario: Tentativa bem-sucedida de cancelamento de um pedido
    Given Estou na tela de Login
    And Eu preencho o campo Email com "danielcursos00@gmail.com"
    And Eu preencho o campo Senha com "dadadada09"
    When Eu clico no botão "Logar"
    Then Eu sou redirecionado para a página "http://localhost:3000/"
    And Eu clico no botão "Pedidos"
    And Eu sou redirecionado para essa página "http://localhost:3000/pedidos"
    And Eu vejo "ID Pedido: 8"
    And Eu clico no botão "Cancelar Pedido"
    And Eu vejo o modal com a mensagem "Cancelado Pedido cancelado com sucesso."