Feature: Cadastro e manutenção de itens no menu

    Scenario: Tentar Exibir um Produto que está cadastrado no banco de dados
        Given um produto existente no banco de dados com id "2"
        When Faço uma Requisição GET para a rota "/view_Produtos/2" 
        Then O status da resposta deve ser 200
        And a resposta JSON deve conter "2", "56789012345678", "Roupas", "Camiseta", "Marca B", "30" e "Cor Verde"

    Scenario: Tentar Exibir um Produto que não está cadastrado no banco de dados
        Given um produto com id "2525" não está cadastrado no banco de dados
        When Faço uma Requisição GET para a rota "/view_Produtos/2525" 
        Then O Status da resposta deve ser 404
        And a resposta deve conter o detalhe "Product not found"

    Scenario: Tentar Atualizar um produto que está cadastrado no banco de dados
        Given um produto existente no banco de dados com id "1"
        When uma requisição PUT é enviada para a rota "/update_produto/1", com ID "1",CNPJ da loja "12345678901234", categoria "Eletrônico", nome "Monitor XGB", Marca "LG", preço "1000" e Especificações "16 polegadas"
        Then o status da resposta deve ser 200
        And A resposta JSON Deve conter "1", "12345678901234", "Eletrônico", "Monitor XGB", "LG", "1000" e "16 polegadas"
    
    Scenario: Tentar Atualizar um produto que não está cadastrado no banco de dados
        Given um produto com id "2525" não está cadastrado no banco de dados
        When uma requisição PUT é enviada para a rota "/update_produto/2525", com ID "2525", categoria "Eletrônico", nome "Monitor XGB", Marca "LG", preço "1000" e Especificações "16 polegadas"
        Then O Status da resposta deve ser 404
        And a resposta deve conter o detalhe "Product not found"

    Scenario: Tentar Excluir um produto que está cadastrado no banco de dados
        Given um produto existente no banco de dados com id "4"
        When uma requisição é enviada para a rota "/del_produtos/4"
        Then O status da resposta deve ser 200
        And A resposta JSON Deve conter "Product Deleted"

    Scenario: Tentar Excluir um produto que não está cadastrado no banco de dados
        Given Um produto com id "40" não está cadastrado no banco de dados
        When uma requisição é enviada para a rota "/del_produtos/40"
        Then O status da resposta deve ser 404
        And a resposta deve conter o detalhe "Product not found"

    Scenario: Adicionar um Produto ao menu geral com um ID já utilizado
        Given um produto existente no banco de dados com id "3"
        When uma Requisição é enviada para a rota /add_produtos/ com id "3", com cnpj da loja "56789012345678", categoria "esportes", nome "bola futebol", da marca "adidas", Preço "50" e Especificações "..."
        Then O Status da resposta deve ser 404
        And a resposta deve conter o detalhe "id already registered"
    
    Scenario: Adicionar um Produto ao menu geral com um ID ainda não utilizado
        Given um produto com id "3535" não está cadastrado no banco de dados
        When uma Requisição é enviada para a rota /add_produtos/ com id "3535", com cnpj da loja "56789012345678", categoria "Roupas", nome "Meia", da marca "adidas", Preço "23" e Especificações "35-42"
        Then O Status da resposta deve ser 200
        And A resposta JSON Deve conter "3535", "56789012345678", "Roupas", "Meia", "adidas", "23" e "35-42"

    Scenario: Exibir todos os produtos do banco de dados
        Given produtos existentes no banco de dados com id "1", "2", "3"
        When Faço uma Requisição GET para a rota "/All_Produtos/" 
        Then O status da resposta deve ser 200
        And a resposta JSON deve conter "1", "12345678901234", "Eletrônico", "Monitor XGB", "LG", "1000" e "16 polegadas", "2", "56789012345678", "Roupas", "Camiseta", "Marca B", "30" e "Cor Verde", "3", "56789012345678", "esportes", "bola futebol", "adidas", "50" e "..."





