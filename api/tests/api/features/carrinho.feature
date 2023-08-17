Feature: Carrinho de Compras

Scenario: Retornar itens de um pedido inexistente
Given: No banco de dados, não existe um pedido para o cpf "98765432100"
When: Faço uma requisição do tipo GET para a rota /pedidos/98765432100
Then: O servidor retorna um erro com detalhe "Pedido não encontrado"

Scenario: Retornar itens de um pedido
Given: No banco de dados, existe um pedido para o cpf "98765432100"
When: Faço uma requisição do tipo GET para a rota /pedidos/98765432100
Then: O servidor retorna id_pedido "10", quantidade "2", id_produto "1" e id_item "48"

Scenario: Inserir um item ao carrinho de um cliente que ainda não tem um pedido
Given: Sou um Usuario registrado no sistema com o cpf igual a “98765432100” 
And: No banco de dados, temos um produto com id_produto igual a "1". 
When: Faço uma requisição do tipo POST para a rota /novo-item/ informando o id_produto “1”, meu cpf e a quantidade 2
And: O servidor processa minha requisição, executando a função post_item_cart, e não é encontrado um pedido  com status = “1” que indica que o cliente ainda não tem nenhum item no carrinho
Then: Recebo uma mensagem informando que foi criado um pedido com id_item "1" e o produto com id “1” foi adicionado ao meu carrinho com quantidade “2” com sucesso.

Scenario: Tentativa de inserção de um produto em um carrinho que já possui um pedido no carrinho
Given: Sou um Usuario registrado no sistema com o cpf igual a “98765432100” 
And: No banco de dados, temos um produto com id_produto igual a "1".
And: No banco de dados, temos um pedido com cpf_usuario igual a “98765432100”, e id_pedido = “1”
When: Faço uma requisição do tipo POST para a rota /novo-item/ informando o id_produto “1”, meu cpf e a quantidade 2
Then: a função atualiza a quantidade do item que tem o produto com id = “1”


Scenario: Tentativa de inserção de um produto em um carrinho que não é da mesma loja que o produto que já está no carrinho
Given: Sou um Usuario registrado no sistema com o cpf igual a “98765432100” 
And: No banco de dados, tenho um item que tem um produto com id_produto “1” que é da loja com cnpj “12345678901234”
When: Faço requisição do tipo POST para a rota /novo-item/ informando o id_produto “2, meu cpf “98765432100” e a quantidade “2” uma inserção de outro item que tem um produto que é da loja com cnpj “56789012345678”
Then: O servidor retorna um erro com detalhe "produto inserido não é da mesma loja que os produtos do carrinho"