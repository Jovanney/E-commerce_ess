from selenium.webdriver.common.by import By
from time import sleep
from features.steps.driver import iniciar_driver
from behave import *

@given(u': Estou na tela de Login')
def step_impl(context):
    context.driver = iniciar_driver()
    context.driver.get("http://localhost:3000/sign-in")
    assert context.driver.current_url == "http://localhost:3000/sign-in"
    sleep(1)

@given(u': Eu preencho o campo Email com "{email}"')
def step_impl(context, email):
    email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[1]/input')
    email_element.send_keys(email)
    sleep(1)

@given(u': Eu preencho o campo Senha com "{senha}"')
def step_impl(context, senha):
    password_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[2]/input')
    password_element.send_keys(senha)
    sleep(1)

@when(u': Eu clico no botão "Logar"')
def step_impl(context):
    login_button = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/button')
    login_button.click()
    sleep(1)

@then(u': O cliente é redirecionado para a página "{url}"')
def step_impl(context, url):
    assert context.driver.current_url == url