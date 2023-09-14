Feature: Cadastro e manutenção de Usuário

Scenario: Criação de conta de cliente com sucesso

Given O Usuário Está na página "sign-up-cliente"
When O Usuário preenche o campo Email com "jovanne4y@gmail.com"
And O Usuário preenche o campo Senha com "321321321"
And O Usuário preenche o campo Re-escrever Senha com "321321321"
And O Usuário preenche o campo Cpf com "45638459752"
And O Usuário preenche o campo Nome com "Jovanney"
And O Usuário clica no botão "Criar Conta"
Then o Usuário deve ver a página inicial "http://localhost:3000/"
