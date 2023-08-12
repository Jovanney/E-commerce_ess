Scenario: Teste main 1

Scenario: Teste dev 1

Scenario: Teste dev 2

Scenario: Teste questao 14(depois do ajuste)

Scenario : Cancelar pedido logado em sua conta
Given: Usuário “Italo Felipe de Andrade” está em “Histórico de pedidos"
And: A opção “Cancelar pedido” está disponível
When: O usuário clica em “cancelar pedido”
And: Ele digita a senha para confirmar o cancelamento
Then: Pedido é cancelado
And: Pedido é retirado da lista de pedidos

Scenario: Cancelar pedido fora do prazo
Given: Usuário “Italo Felipe de Andrade” está em “Histórico de pedidos"
And: A opção “Cancelar pedido” está indisponível
When: Usuário clica em “cancelar pedido”
Then: Aparece uma mensagem informando que o pedido não pode ser cancelado
And: Pedido continua na lista de pedidos

Scenario: Adicionar produto ao carrinho de compras da mesma loja
Given: Usuário está na página do menu geral
When: Ele clica na opção “adicionar ao carrinho” de um item X
And: Item X é da mesma loja dos outros produtos em seu carrinho
Then: Carrinho é atualizado com o novo item, adicionado pelo usuário

Scenario: Adicionar produto ao carrinho de compras de lojas diferentes
Given: Usuário está na página do menu geral
When: Ele clica na opção “adicionar ao carrinho” de um item X
And: Item X não é da mesma loja dos outros produtos em seu carrinho
Then: Aparece uma mensagem informando ao cliente que o item X não pode ser adicionado ao carrinho pois é de uma loja diferente
And: carrinho se mantém igual

Scenario: Cliente deseja visualizar as informações dos pedidos feitos anteriormente
Given: Usuário está na página “histórico de pedidos”
And: Existe no mínimo um pedido no histórico de pedidos
When: Usuário clica em algum pedido
Then: Aparece uma página com as informações do pedido, como data, preço, entre outras

