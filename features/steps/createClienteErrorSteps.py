from selenium.webdriver.common.by import By
from time import sleep
from features.steps.driver import iniciar_driver
from behave import *

@given(u'O Usuário Está na página "{pagina}"')
def step_impl(context, pagina):
    context.driver = iniciar_driver()
    context.driver.maximize_window()
    context.driver.get(f"http://localhost:3000/{pagina}")
    sleep(1)

@when(u'O Usuário preenche o campo Email com "{valor}"')
def step_impl(context, valor):
    email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[1]/input')
    email_element.send_keys(valor)
    assert email_element.get_attribute('value') == valor
    sleep(1)

@when(u'O Usuário preenche o campo Senha com "{valor}"')
def step_impl(context, valor):
    email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[2]/input')
    email_element.send_keys(valor)
    assert email_element.get_attribute('value') == valor
    sleep(1)
    
@when(u'O Usuário preenche o campo Re-escrever Senha com "{valor}"')
def step_impl(context, valor):
    email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[3]/input')
    email_element.send_keys(valor)
    assert email_element.get_attribute('value') == valor
    sleep(1)
    

@when(u'O Usuário preenche o campo Cpf com "{valor}"')
def step_impl(context, valor):
    email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[4]/input')
    email_element.send_keys(valor)
    assert email_element.get_attribute('value') == valor
    sleep(1)
    

@when(u'O Usuário preenche o campo Nome com "{valor}"')
def step_impl(context, valor):
    email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[5]/input')
    email_element.send_keys(valor)
    assert email_element.get_attribute('value') == valor
    sleep(1)
    

@when(u'O Usuário clica no botão "{botao}"')
def step_impl(context, botao):
    botao_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/button')
    botao_element.click()
    

@then(u'o Usuário deve ver uma mensagem informando que "{mensagem}"')
def step_impl(context, mensagem):
    sleep(3)
    error_message_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[3]/p')
    assert error_message_element.text == mensagem

