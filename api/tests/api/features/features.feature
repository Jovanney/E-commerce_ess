Feature: Cadastro e manutenção de itens no menu
Scenario: Tentar Exibir um Produto que está cadastrado no banco de dados
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero Visualizar o produto com ID 2
And: Existe um produto com ID 2 na entidade Pedidos, com cnpj da loja “56789012345678”, categoria “Roupas”, nome “Camiseta”, da marca “Marca B”, Preço “29.99” e Especificações “Cor Verde”
When: Faço uma Requisição GET para a rota /produtos/2, Usando o ID do produto que quero consultar como parâmetro PATH
Then: É mostrado na tela todas as características(atributos) do produto com ID 2  

Scenario: Tentar Exibir um Produto que não está cadastrado no banco de dados
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero Visualizar o produto com ID 2
And: Não existe um produto com ID 2 na entidade Pedidos.
When: Faço uma Requisição GET para a rota /produtos/2, Usando o ID do produto que quero consultar como parâmetro PATH
Then: É retornado uma HTTPException informando que o produto não foi encontrado no banco de dados

Scenario: Adicionar um Produto ao menu geral com um ID ainda não utilizado
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero adicionar o produto com ID 3, com a loja de cnpj 56789012345678, com o nome igual a “camisa de linho”, da marca “ciao”, preço “500” e especificações “100% Linho” 
And: Não existe um produto com ID 3
And: Existe uma loja com cnpj 56789012345678
When: Faço uma Requisição POST para a rota /produtos/3, usando o ID do produto que quero inserir como parâmetro path
Then: O produto é adicionado a entidade “produto” 
And: É retornado o produto criado

Scenario: Adicionar um Produto ao menu geral com um ID já utilizado
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero adicionar o produto com ID 3, com a loja de cnpj 56789012345678, com o nome igual a “camisa de linho”, da marca “ciao”, preço “500” e especificações “100% Linho” 
And: Já existe um produto com ID 3
And: Existe uma loja com cnpj 56789012345678
When: Faço uma Requisição POST para a rota /produtos/3, usando o ID do produto que quero inserir como parâmetro path
Then: É retornado uma HTTPException informando que o ID já foi cadastrado
And: O produto não é adicionado ao banco de dados

Scenario: Tentar Excluir um produto que está cadastrado no banco de dados
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero Excluir o Produto com ID 2
And: Existe um produto com ID 2 na entidade Pedidos, com cnpj da loja “56789012345678”, categoria “Roupas”, nome “Camiseta”, da marca “Marca B”, Preço “29.99” e Especificações “Cor Verde”
When: Faço uma requisição DELETE para a rota /produtos/2, Usando o ID do produto que quero Deletar como parâmetro PATH
Then: O Produto é apagado da entidade “Produtos” do banco de dados
And: É retornada uma mensagem “Product Deleted” para o usuário 

Scenario: Tentar Excluir um produto que não está cadastrado no banco de dados
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero Excluir o Produto com ID 2
And: Não Existe um produto com ID 2 na entidade Pedidos
When: Faço uma requisição DELETE para a rota /produtos/2, Usando o ID do produto que quero Deletar como parâmetro PATH
Then: É retornado uma HTTPException informando que o produto não foi encontrado na base de dados

Scenario: Tentar Atualizar um produto que está cadastrado no banco de dados
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero atualizar o produto com ID 1
And: Existe um produto com ID 1 na entidade Pedidos, com cnpj da loja “56789012345678”, categoria “Roupas”, nome “Camiseta”, da marca “Marca B”, Preço “29.99” e Especificações “Cor Verde”
When: Faço uma requisição PUT para a rota /update_produto/1, Usando o ID do produto que quero Atualizar como parâmetro PATH e preencho os campos para ID 1,CNPJ da loja “
12345678900”, categoria “Eletrônico”, nome “Monitor XGB”, Marca “LG”, preço “2000” e Especificações “16 polegadas”
Then: O pedido com ID 1 é atualizado na entidade “Produto” no banco dados, sobrescrevendo os seus atributos para  ID 1,CNPJ da loja “
12345678900”, categoria “Eletrônico”, nome “Monitor XGB”, Marca “LG”, preço “2000” e Especificações “16 polegadas”

Scenario: Tentar Atualizar um produto que não está cadastrado no banco de dados
Given: Sou um Usuário Logado no sistema com o cpf igual a "12345678910” e email 123@gmail.com
And: Quero atualizar o produto com ID 1
And: Não Existe um produto com ID 1 na entidade Pedidos
When: Faço uma requisição PUT para a rota /update_produto/1, Usando o ID do produto que quero Atualizar como parâmetro PATH e preencho os campos para ID 1,CNPJ da loja “
12345678900”, categoria “Eletrônico”, nome “Monitor XGB”, Marca “LG”, preço “2000” e Especificações “16 polegadas”
Then: É retornado uma HTTPException informando que o produto não foi encontrado na base de dados



