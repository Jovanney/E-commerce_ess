Feature: Cancelamento de pedidos

Scenario: Tentativa de cancelamento de um pedido inexistente
    Given Que não existe um pedido com ID "20" associado ao CPF "12345678900" no banco de dados
    When Faço uma requisição PUT para "/cancelar_pedido/12345678900/20"
    Then O servidor deve responder com o status "404"
    And A resposta deve conter o detalhe "Pedido não encontrado"

Scenario: Tentativa de cancelar um pedido já cancelado
    Given No banco de dados, tenho um pedido de ID "1" associado ao CPF "12345678900" com id_status "5"
    When Faço uma requisição PUT para "/cancelar_pedido/12345678900/1"
    Then O servidor deve responder com o status "403"
    And a resposta deve conter o detalhe "O pedido já foi cancelado anteriormente"

Scenario: Cancelamento bem-sucedido de um pedido confirmado
    Given No banco de dados, tenho um pedido de ID "3" associado ao CPF "98765432100" com id_status "2"
    When Faço uma requisição PUT para "/cancelar_pedido/98765432100/3"
    Then O servidor deve responder alterando o id_status para "5" para o pedido "3"
    And A resposta deve conter a mensagem "Pedido cancelado com sucesso"

Scenario: Tentativa de cancelar um pedido que não pode ser cancelado
    Given No banco de dados, tenho um pedido de ID "4" associado ao CPF "98765432100" com id_status "3"
    When Faço uma requisição PUT para "/cancelar_pedido/98765432100/4"
    Then O servidor deve responder com o status "403"
    And A resposta deve conter o detalhe "Pedido não pode mais ser cancelado"