# from selenium.webdriver.common.by import By
# from time import sleep
# from features.steps.driver import iniciar_driver
# from behave import *

# @given('Estou na tela de Login')
# def step_impl(context):
#     context.driver = iniciar_driver()
#     context.driver.maximize_window()
#     context.driver.get("http://localhost:3000/sign-in")
#     sleep(1)

# @given('Eu preencho o campo Email com "{email}"')
# def step_impl(context, email):
#     email_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[1]/input')
#     email_element.send_keys(email)
#     sleep(1)

# @given('Eu preencho o campo Senha com "{senha}"')
# def step_impl(context, senha):
#     password_element = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/div/div[2]/input')
#     password_element.send_keys(senha)
#     sleep(1)

# @when('Eu clico no botão "Logar"')
# def step_impl(context):
#     login_button = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/div/form/button')
#     login_button.click()
#     sleep(1)

# @then('Eu sou redirecionado para a página "{url}"')
# def step_impl(context, url):
#     assert context.driver.current_url == url
#     sleep(3)

# @then('Eu clico no botão "Comprar"')
# def step_impl(context):
#     sleep(3)
#     comprar_button = context.driver.find_element(By.XPATH, '/html/body/main/div[1]/section/div/div[1]/button')
#     comprar_button.click()
#     sleep(1)

# @then('Eu vejo o modal com a mensagem "Produto adicionado ao carrinho!"')
# def step_impl(context):
#     # Você pode precisar de um tempo para o modal aparecer
#     modal_message = context.driver.find_element(By.XPATH, '/html/body/main/div[2]/ol/li/div/div[1]')
#     assert modal_message.text == "Produto adicionado ao carrinho!"