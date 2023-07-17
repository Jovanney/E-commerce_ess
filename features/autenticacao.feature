Cenário 1 Cadastrando novo usuário
Given eu estou na tela de Login
And eu clico em “Cadastrar usuário”
Then o modal de Criação de conta aparece
When  eu adiciono todas as informações
And eu clico em Criar
Then eu sou redirecionado para a página principal do e-commerce
And eu consigo ver os produtos do e-commerce

Cenário 2: Recuperando senha de usuário 
Given eu estou na tela de Login 
And eu clico em “Esqueci minha senha” 
Then o modal de Recuperação de senha aparece 
When eu insiro meu endereço de e-mail cadastrado 
And eu clico em Enviar 
Then um e-mail é enviado para mim com instruções para redefinir minha senha 
When eu sigo as instruções do e-mail e redefino minha senha 
And eu volto para a tela de Login 
And eu insiro meu endereço de e-mail e nova senha 
Then eu sou redirecionado para a página principal do e-commerce 
And eu consigo ver os produtos do e-commerce.

Cenário 3: Falha ao recuperar senha de usuário 
Given eu estou na tela de Login 
And eu clico em “Esqueci minha senha” 
Then o modal de Recuperação de senha aparece 
When eu insiro um endereço de e-mail não cadastrado 
And eu clico em Enviar Then uma mensagem de erro é exibida informando que o endereço de e-mail não está cadastrado 
And o modal de Recuperação de senha permanece aberto para que eu possa tentar novamente.

Cenário 4: Falha ao fazer login com credenciais incorretas 
Given eu estou na tela de Login 
When eu insiro um endereço de e-mail ou senha incorretos 
And eu clico em Entrar 
Then uma mensagem de erro é exibida informando que as credenciais estão incorretas 
And o campo de endereço de e-mail e senha são limpos para que eu possa tentar novamente.

Cenário 5: Alterando senha de usuário 
Given eu estou na página principal do e-commerce 
And eu clico em “Minha conta” 
Then a página de Minha conta aparece 
When eu clico em “Alterar senha” 
And eu insiro minha senha atual e minha nova senha 
And eu clico em Salvar 
Then minha senha é alterada com sucesso 
And eu recebo uma mensagem de confirmação de alteração de senha 
And eu posso continuar navegando na página principal do e-commerce e ver os produtos do e-commerce.

Cenário 6: Adicionando um novo endereço de entrega 
Given eu estou na página principal do e-commerce 
And eu clico em “Minha conta” 
Then a página de Minha conta aparece 
When eu clico em “Adicionar novo endereço” 
And eu preencho os campos com as informações do meu novo endereço 
And eu clico em Salvar 
Then meu novo endereço é adicionado com sucesso 
And eu recebo uma mensagem de confirmação de adição de novo endereço 
And eu posso continuar navegando na página principal do e-commerce e ver os produtos do e-commerce.