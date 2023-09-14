from selenium.webdriver.common.by import By
from time import sleep
from features.steps.driver import iniciar_driver
from behave import *

@given('Estou na tela de Login')
def step_impl(context):
    context.driver = iniciar_driver()
    context.driver.maximize_window()
    context.driver.get("http://localhost:3000/sign-in")
    sleep(1)

@given('Eu preencho o campo Email com "{email}"')
def step_impl(context, email):
    email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[1]/input')
    email_element.send_keys(email)
    sleep(1)

@given('Eu preencho o campo Senha com "{senha}"')
def step_impl(context, senha):
    password_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[2]/input')
    password_element.send_keys(senha)
    sleep(1)

@when('Eu clico no botão "Logar"')
def step_impl(context):
    login_button = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/button')
    login_button.click()
    sleep(1)

@then('Eu sou redirecionado para a página "{url}"')
def step_impl(context, url):
    assert context.driver.current_url == url
    sleep(3)

@then('Eu clico no botão "Pedidos"')
def step_impl(context):
    # Você precisa especificar o XPath correto para o botão "Pedidos"
    sleep(3)
    pedidos_button = context.driver.find_element(By.XPATH, '/html/body/main/nav/div/div[3]/a[2]')
    pedidos_button.click()
    sleep(1)
    
@then('Eu sou redirecionado para essa página "{url}"')
def step_impl(context, url):
    assert context.driver.current_url == url
    
@then('Eu vejo "ID Pedido: {pedido_id}"')
def step_impl(context, pedido_id):
    id_pedido = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div/div[1]')
    assert id_pedido.text == "ID Pedido: {}".format(pedido_id)

@then('Eu clico no botão "Cancelar Pedido"')
def step_impl(context):
    sleep(3)
    cancelar_pedido_button = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div/button')
    cancelar_pedido_button.click()
    sleep(1)

@then('Eu vejo o modal com a mensagem "{mensagem}"')
def step_impl(context, mensagem):  # Pode precisar de um tempo para o modal aparecer
    status_text_element = context.driver.find_element(By.XPATH, '/html/body/main/div[2]/ol/li/div/div[1]')
    message_text_element = context.driver.find_element(By.XPATH, '/html/body/main/div[2]/ol/li/div/div[2]')

    combined_text = status_text_element.text + " " + message_text_element.text

    assert combined_text == mensagem