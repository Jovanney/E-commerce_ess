Feature: Carrinho de Compras
Scenario: Retornar itens de um pedido inexistente
Given No banco de dados, não existe um pedido para o cpf "98765432111"
When Faço uma requisição GET para a rota "/pedidos/98765432111"
Then o status da resposta deve ser "200"
And a resposta deve conter o detalhe "Pedido não encontrado"

Scenario: Retornar itens de um pedido
Given No banco de dados, existe um pedido para o cpf "98765432100"
When Faço uma requisição GET para a rota "/pedidos/98765432100"
Then O servidor retorna id_pedido "14", quantidade "1", id_produto "3" e id_item "51"

Scenario: Inserir um item ao carrinho de um cliente que ainda não tem um pedido
Given um produto existente no banco de dados com id_produto "1"
When Faço uma requisição POST para a rota "/novo-item/" com id_produto "1", usuario_cpf "12345678900"  e quantidade "1"
Then o status da resposta deve ser "422"
And é criado um pedido com id_item "1", e o produto com id "1" foi adicionado ao meu carrinho com quantidade "1".

Scenario: Tentativa de inserção de um produto em um carrinho que não é da mesma loja que o produto que já está no carrinho
Given No banco de dados, existe um item que tem um produto com id_produto "1"
When Faço requisição POST para a rota "/novo-item/" com id_produto "2", cpf "98765432100" e a quantidade "2"
Then o status da resposta deve ser "422"


