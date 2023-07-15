Scenario 1: Loja cadastrar novos itens no menu
Given: Administrador/Loja está na página “Minha loja”  
And: Ele possui as informações sobre os produtos ainda não adicionados em uma tabela
When: O administrador/loja seleciona o botão “adicionar item” 
And: Coloca o ID do produto
Then: O produto já está cadastrado na página “Minha loja”, com todas as informações já resgatadas pelo ID 

Scenario 2: Loja excluir itens cadastrados
 Given: Administrador/Loja está na página “Minha loja”
 When: Ele clica na opção de excluir o item
 And: Ele clica na confirmação “Certeza que deseja excluir permanentemente esse item??”
 Then: O item é deletado do banco de dados da aplicação

Scenario 3: remover produto do carrinho de compras
Given: Usuário está na página do menu geral
When: Ele clica na opção “remover do carrinho” de um item X
And: Item X não é da mesma loja dos outros produtos em seu carrinho
Then: Aparece uma mensagem informando ao cliente que o item Xfoi removido do carrinho

Scenario 4:  saindo do carrinho de compras
Given: Usuário está na página do menu geral
When: Ele clica na opção “sair do carrinho”
Then: Usuario está em outra página


Scenario 5:  adicionando mais uma unidade há um item
Given: Usuário está na página do menu geral
And:  Usuário visualiza apenas uma unidade do item
And:  Ele visualiza um botão ao lado do item
When: Ele clica no botão 
Then: o item agora possui duas unidades