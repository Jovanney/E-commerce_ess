# E-commerce

#### Requisitos

| Ferramenta        | Versão     | Descrição                                             |
|-------------------|------------|-------------------------------------------------------|
| Visual Code       | >= 4.9.0   | IDE de desenvolvimento padrão                         |
| Python            | >= 3.11    | linguagem                                             |
| poetry            | >= 1.5.1   | gerenciador de dependências                           |
| Docker            | >= 20.10.2 | Container Engine                                      |
| Git               | -          | Controle de versões                                   |
| Node              | >= 18.12.1 | Web                                                   |
| Npm               | >= 9.6.2   | gerenciador de versões, gerenciador de pacotes        |
| Linux / Windows 10| -          | Sistema operacional                                   |

<hr />

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

### Como executar o projeto

- Clone este repositório.
  - `$ git clone {URL deste repositório} `
- Verifique se o python 3.11 está devidamente instalado e com as variáveis de ambiente configuradas.

  - `$ python --version`

- Verifique se o Node.js 18.12.1 está devidamente instalado.

  - `$ Node --version`

### instalando o poetry 

- https://python-poetry.org/docs/ 

- obs depois da instalação verificar o PATH

### Migration (Alembic)
- A instalação ja deveria ter sido feita no momento do poetry install pois ele se encontra como dependencia dentro do poetry.lock

### Subir a imagem do docker
- Para subir o serviço
  - docker run -d -p 5438:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres postgres:latest
  
- Para derrubar o serviço
  - docker ps
  - docker stop <ID ou nome do contêiner>

### SGBD
- Nesse link é possível verificar os documentos que estão armazenados no postgres para serem enviados posteriormente
- http://localhost:5438
- login: postgres
- senha: postgres

### Comandos básicos do projeto

  -npm install: instala as dependencias que se encontram no arquivo package.json

  -npm run startpy: entra no ambiente virtual e instala dependencias que se encontram no arquivo poetry.lock

  -npm run dev :  permite que o aplicativo seja executado com recarga de código quente, relatórios de erros e muito mais

  Abra [http://localhost:3000](http://localhost:3000) com o navegador para ver o resultado.


### Comandos basicos do alembic
- alembic revision -m "<mensagem>": Cria uma nova revisão/migração com a mensagem fornecida. Você pode adicionar suas alterações de esquema dentro desta revisão. (não costumamos usar essa revision)

- alembic upgrade <target>: Executa todas as migrações necessárias para atualizar o banco de dados para o alvo especificado. Por exemplo, alembic upgrade head atualiza para a revisão mais recente.

- alembic upgrade 'head' atualiza para a revisão mais recente.

- alembic downgrade <target>: Reverte as migrações aplicadas para levar o banco de dados de volta ao alvo especificado. Por exemplo, alembic downgrade base reverte todas as migrações.

- alembic current: Mostra a revisão atual do banco de dados.

- alembic history: Lista todas as revisões aplicadas no banco de dados.

- alembic show <target>: Mostra todas as migrações necessárias para atualizar o banco de dados para o alvo especificado.

- alembic stamp <target>: Marca o banco de dados com a revisão especificada, sem executar as migrações. Isso é útil para indicar que uma migração específica foi aplicada manualmente.

- alembic revision --autogenerate -m "<mensagem>": Gera automaticamente uma nova revisão/migração baseada nas diferenças detectadas entre o estado atual do banco de dados e os modelos declarativos. A mensagem é opcional, mas é recomendável fornecer uma descrição significativa.

<hr />

