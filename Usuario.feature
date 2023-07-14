Scenario 1: Cadastro com email já utilizado
Given: Usuário “Vitor Modesto Leitão” com email “vml2” já está cadastrado no sistema
When: Usuário clica na opção de fazer cadastro
And: Coloca as credenciais já cadastradas
Then: Aparece uma mensagem informando-o que essas credenciais já foram utilizadas

Scenario 2: Cadastro com dados corretos
Given: Usuário “Vitor Modesto Leitão” com email “vml2” ainda não está cadastrado no sistema
When: Usuário clica na opção de fazer cadastro
And: Coloca as credenciais ainda não cadastradas
Then: Aparece uma mensagem informando-o que o cadastro foi bem sucedido 
And: Informações são adicionadas ao banco de dados

Scenario 3: Login com dados cadastrados
Given: Usuário não está logado na aplicação 
And: Os dados “vitor modesto leitao” e “vml2@cin.ufpe.br” já estão cadastrados no sistema
When: Usuário coloca os seus dados no campo de login
And: Usuário clicar na opção “entrar”
Then: Aparece uma mensagem informando que o cliente entrou em sua conta corretamente

Scenario 4: Login com dados não cadastrados
Given: Usuário não está logado na aplicação 
And: Os dados “vitor modesto leitao” e “vml2@cin.ufpe.br” não estão cadastrados no sistema
When: Usuário coloca os seus dados no campo de login
And: Usuário clicar na opção “entrar”
Then: Aparece uma mensagem informando que os dados não estão cadastrados no sistema

scenario 5: teste
given x
and y
when z
and w

