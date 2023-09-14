Feature: login
Scenario: Login com dados cadastrados de Jovanney
    Given : Estou na tela de Login
    And : Eu preencho o campo Email com "jovanney@gmail.com"
    And : Eu preencho o campo Senha com "321321321"
    When : Eu clico no botão "Logar"
    Then : O cliente é redirecionado para a página "http://localhost:3000/"