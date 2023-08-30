Feature: Historico de Pedidos

Scenario: Usuário acessando histórico e não encontrando nenhum pedido
    Given Sou um Usuario registrado no sistema com o cpf igual a "11111111111"
    And No banco de dados, não tenho nenhum Pedido associado ao meu cpf "11111111111"
    When Faço uma requisição do tipo GET para a rota "/pedidos/11111111111"
    Then o servidor retorna o histórico de pedidos do usuário de cpf "11111111111"
    And Recebo uma resposta indicando "Não há histórico de pedidos para este usuário."


Scenario: Usuário acessando histórico de pedidos
    Given Sou um usuário registrado no sistema com o cpf "12345678900"
    And No banco de dados, existe um pedido com ID "1", cpf_usuario "12345678900", preco_total "699.98" e id_status "5"
    And Associado ao pedido "1", temos um item com quantidade "3" e nome_produto "Celular"
    And Associado ao pedido "1", temos um item com quantidade "5" e nome_produto "Camiseta"
    When Faço uma requisição do tipo GET para a rota "/pedidos/12345678900" 
    Then Vejo os detalhes do pedido com ID "1", preço total "699.98", id_status "5" e os seguintes produtos:
    And O produto "Celular" está associado ao pedido com quantidade "3"
    And O produto "Camiseta" está associado ao pedido com quantidade "5"