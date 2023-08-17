Feature: Cancelamento de pedidos


Scenario: Cancelamento de um pedido que não existe
Given: No banco de dados, não existe um pedido com ID "5" para o cpf "21111111111"
When: Faço uma requisição do tipo PUT para a rota /cancelar_pedido/21111111111/5
Then: O servidor retorna um erro com detalhe "Pedido não encontrado"


Scenario: Tentativa de cancelar um pedido já cancelado
Given: No banco de dados, tenho um pedido de ID "1" associado ao CPF "11111111111" com status "5"
When: Faço uma requisição do tipo PUT para a rota /cancelar_pedido/11111111111/1
Then: O servidor retorna um erro com detalhe "O pedido já foi cancelado anteriormente"


Scenario: Cancelamento bem-sucedido de um pedido confirmado
Given: No banco de dados, tenho um pedido de ID "3" associado ao CPF "21111111111" com status "2"
When: Faço uma requisição do tipo PUT para a rota /cancelar_pedido/21111111111/3
Then: O servidor atualiza o status do pedido para "5"
And Retorna uma resposta com a mensagem "Pedido cancelado com sucesso"

Scenario: Tentativa de cancelar um pedido que não pode ser cancelado
Given: No banco de dados, tenho um pedido de ID "5555" associado ao CPF "11111111111" com um status “3” ou “4”
When: Faço uma requisição do tipo PUT para a rota /cancelar_pedido/11111111111/5555
Then: O servidor retorna um erro com detalhe "Pedido não pode mais ser cancelado"


