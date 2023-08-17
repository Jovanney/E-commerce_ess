Feature: Historico de Pedidos

Scenario: Usuário acessando histórico e não encontrando nenhum pedido
Given Sou um Usuario registrado no sistema com o cpf igual a "11111111111"
And No banco de dados, não tenho nenhum Pedido associado ao meu cpf
When Faço uma requisição do tipo GET para a rota /pedidos/11111111111
Then o servidor retorna o histórico de pedidos do usuário de cpf "11111111111"
And Recebo uma resposta indicando "Usuário sem pedidos"


Scenario: Usuário acessando histórico de pedidos
Given: Sou um usuário registrado no sistema com o cpf "12345678910".
And: Estou logado no sistema.
And: No banco de dados, existe um pedido com ID 1, cpf_usuario "12345678910", preço total de 1500 e status diferente de "não confirmado".
And: Associado a esse pedido, temos um item com quantidade de 2 e nome_produto "Produto X".
When: Faço uma requisição do tipo GET para a rota /pedidos/12345678910 utilizando meu CPF como parâmetro.
Then: Vejo os detalhes do pedido com ID 1, preço total de 1500, e a lista de itens associados, incluindo um item com quantidade 2 e nome "Produto X".

Scenario: Retornar detalhes de múltiplos pedidos confirmados de um cliente
Given: Sou um usuário registrado no sistema com o cpf "12345678910".
And: Estou logado no sistema.
And: No banco de dados, existe um pedido com ID 1, cpf_usuario "12345678910", preço total de 1500 e status diferente de "não confirmado".
And: Associado a esse pedido com ID 1, temos um item com quantidade de 2 e nome_produto "Produto X".
And: No banco de dados, existe um segundo pedido com ID 2, cpf_usuario "12345678910", preço total de 1000 e status diferente de "não confirmado".
And: Associado a esse segundo pedido com ID 2, temos um item com quantidade de 3 e nome_produto "Produto Y".
When: Faço uma requisição do tipo GET para a rota /pedidos/12345678910 utilizando meu CPF como parâmetro.
Then: Vejo os detalhes do pedido com ID 1, preço total de 1500, e a lista de itens associados, incluindo um item com quantidade 2 e nome "Produto X".
And: Vejo também os detalhes do pedido com ID 2, preço total de 1000, e a lista de itens associados, incluindo um item com quantidade 3 e nome "Produto Y".




