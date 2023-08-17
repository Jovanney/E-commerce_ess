Feature: Carrinho de Compras

Scenario: Retornar itens de um pedido inexistente
Given: No banco de dados, não existe um pedido para o cpf "98765432100"
When: Faço uma requisição do tipo GET para a rota /pedidos/98765432100
Then: O servidor retorna um erro com detalhe "Pedido não encontrado"

