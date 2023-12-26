from playwright.sync_api import sync_playwright
import time
import os
from dotenv import load_dotenv
import logging
import requests
import random
import sys

load_dotenv('credentials.env')

WAIT_TIME = 3 #Wait time between runs, in minutes
LOGIN_URL = 'https://<dealership>.dealernetworkflow.com.br/' #Change it to your DealerNet access URL
DEALERNET_USERNAME = '<USERNAME>' #Username of DealerNet's account
DEALERSHIP = '<DEALERSHIP NAME>' #Dealership name/branch to be included on the message
username = os.getenv('USERNAME_CR')
password = os.getenv('PASSWORD_CR')
url = '<YOUR WHATSAPP API CALL>'
headers = {
    'API_KEY': 'YOUR API KEY',
    'Content-Type': 'application/json'
    }

NOTIFY_ERROR = False
TMP_FILE_PATH = 'last_run.tmp' #Save the amount of leads of the last run. For multiple scripts runing on the same folder use an individual file for each script.

def get_last_run_n_leads():
    if os.path.exists(TMP_FILE_PATH):
        with open(TMP_FILE_PATH, 'r') as file:
            return int(file.read())
    return 0

def set_last_run_n_leads(value):
    with open(TMP_FILE_PATH, 'w') as file:
        file.write(str(value))

def error_exception(msg):
    if NOTIFY_ERROR:
        dataException = {
                "contact": "<contact number for errors, if necessary>",
                'message': msg
            }
        requests.post(url, headers=headers, json=dataException)
    logging.error(msg, exc_info=True)
    print(msg)
    sys.exit()

#logging file for errors
logging.basicConfig(filename='playwright_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

boolLead = True

def run_script():
    global boolLead
    lastRunNLeads = get_last_run_n_leads()

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport=None)
            page = context.new_page()
            page.goto(LOGIN_URL)
            page.wait_for_load_state()
        
        except Exception as e:
            msg = f'Erro ao acessar website: {e}'
            error_exception(msg)

        try:
            page.wait_for_selector('#vUSUARIO_IDENTIFICADORALTERNATIVO')
            time.sleep(2)
            page.fill('#vUSUARIO_IDENTIFICADORALTERNATIVO', username)
            time.sleep(2)
            page.fill('#vUSUARIOSENHA_SENHA', password)
            page.wait_for_selector('#IMAGE3')
            page.click('#IMAGE3')
        
        except Exception as e:
            msg = f'Erro ao logar: {e}'
            error_exception(msg)       
        
        try:
            page.wait_for_selector('button:text-is("Veículo")')
            page.click('button:text-is("Veículo")')  # Menu Veiculo
        
        except Exception as e:
            msg = f'Erro ao abrir menu Veículo: {e}'
            error_exception(msg)

        try:
            page.wait_for_selector('//a[contains(@id, "Atendimento")]')
            page.hover('//a[contains(@id, "Atendimento")]')  # Atendimento
        
        except Exception as e:
            msg = f'Erro ao abrir menu Atendimento: {e}'
            error_exception(msg)
        
        try:
            page.wait_for_selector('span:text-is("Quadro de Atendimentos")')
            page.hover('span:text-is("Quadro de Atendimentos")')  # Quadro de 
            
        except Exception as e:
            msg = f'Erro ao abrir Quadro de atendimentos: {e}'
            error_exception(msg)

        try:
            page.wait_for_selector('span:text-is("Recepção")')
            page.click('span:text-is("Recepção")')  # Recepção

        except Exception as e:
            msg = f'Erro ao abrir Recepção: {e}'
            error_exception(msg)

        try:
            page.wait_for_selector('iframe[src*="wp_atendimentorecepcao.aspx"]')
            frameElement = page.query_selector('iframe[src*="wp_atendimentorecepcao.aspx"]')
            frame = frameElement.content_frame()
        
        except Exception as e:
            msg = f'Erro ao carregar iframe de atendimentos: {e}'
            error_exception(msg)
            
            
        try:
            time.sleep(5)
            frame.click('#W0073IMGCONSULTAR')
            time.sleep(5)

        except Exception as e:
            msg = f'Erro ao clicar no botão para atualizar leads: {e}'
            error_exception(msg)

        elementExists = True
        nLeads = 1
        try:
            while elementExists:
                formattedNumber = str(nLeads).zfill(4)
                elementExists = frame.query_selector(f'tr#W0073GridContainerRow_{formattedNumber}')
                if elementExists:
                    if boolLead:
                        leadDate = frame.inner_text(f'#span_W0073vRECEPCAO_DATACRIACAO_{formattedNumber}')
                        leadClient = frame.inner_text(f'#span_W0073vRECEPCAO_NOME_{formattedNumber}')
                        leadCar = frame.inner_text(f'#span_W0073vFAMILIAVEICULO_DESCRICAO_{formattedNumber}')
                        leadColor = frame.inner_text(f'#span_W0073vCOR_DESCRICAO_{formattedNumber}')
                        dataLead = {
                            "contact": "<YOUR GROUP OR CONTACT NUMBER TO GET NOTIFIED>",
                            'message': '['+DEALERSHIP+'] ' + 'Lead encontrado: ' + leadDate + ' | ' + leadClient + ' | ' + leadCar + ' | ' + leadColor
                        }
                        print('['+DEALERSHIP+'] ' + 'Lead encontrado: ' + leadDate + ' | ' + leadClient + ' | ' + leadCar + ' | ' + leadColor)
                        requests.post(url, headers=headers, json=dataLead)
                        time.sleep(2)
                    nLeads += 1
                    print(nLeads)
                else:
                    nLeads -= 1
                    print('nLeads: '+str(nLeads))
                    print('lastRunNLeads: '+str(lastRunNLeads))
                    if nLeads == 0:
                        boolLead = True
                        print('Nenhum lead encontrado.')
                    elif lastRunNLeads == nLeads:
                        boolLead = False
                    else:
                        if lastRunNLeads == 0:
                            boolLead = False
                        else:
                            boolLead = True
        
        except Exception as e:
            msg = f'Erro ao processar tabela de leads: {e}'
            error_exception(msg)

        lastRunNLeads = nLeads
        set_last_run_n_leads(lastRunNLeads)
            
        #### BYPASS FOR EXPIRING SESSION (IF RUNNING WITHOUT LOGOUT) ####
        # elementVisible = page.is_visible('tbody.x-btn-small.x-btn-icon-small-left #ext-gen231')

        # if elementVisible:
        #     page.click('tbody.x-btn-small.x-btn-icon-small-left #ext-gen231')
        # else:
        #     print('No expiring session message found, ignoring.')
        ######################################

        try:
            time.sleep(5)
            page.click(f'button:has-text("{DEALERNET_USERNAME}")')
            time.sleep(2)
            page.click('span:text-is("Logout")')
            time.sleep(2)
        
        except Exception as e:
            msg = f'Erro ao deslogar: {e}'
            error_exception(msg)
        
        finally:
            browser.close()

while True:
    run_script()
    randSleep = random.uniform(WAIT_TIME*60 - 15, WAIT_TIME*60 + 15)
    time.sleep(randSleep)