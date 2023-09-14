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

@then('Eu vejo "Preço Total: R$ {preco}"')
def step_impl(context, preco):
    preco_total = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div/div[2]')
    assert preco_total.text == "Preço Total: R$ {}".format(preco)

@then('Eu vejo "Status: {status}"')
def step_impl(context, status):
    status_pedido = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div/div[3]')
    assert status_pedido.text == "Status: {}".format(status)

@then('Eu vejo "Itens do Pedido:"')
def step_impl(context):
    itens_pedido_label = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div/h3')
    assert itens_pedido_label.text == "Itens do Pedido:"

@then('Eu vejo "{quantidade}x {item}"')
def step_impl(context, quantidade, item):
    item_pedido = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div/ul/li')  # Ajuste o XPath se houver múltiplos <li>!
    assert item_pedido.text == "{}x {}".format(quantidade, item)