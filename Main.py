import pyautogui as pa
import keyboard
import acoes_tibia as acoes
import constants as ct
import json
import threading
from pynput.keyboard import Listener
from pynput import keyboard
import my_thread
import os
from multiprocessing import Manager, Process
import time
from importlib import reload
reload(acoes)

# Evento de controle de thread
th_event = threading.Event()

# Função para matar monstros
def matar_monstros():
    while acoes.acoes.check_battle() is None:
        if th_event.is_set():  # Verifica a flag de parada
            return

        pa.press('space')  # Ataca o monstro

        if th_event.is_set():  # Verifica novamente para evitar ações desnecessárias
            return
        
        try:
            alvo = pa.locateOnScreen('prints/alvo_vermelho.png', confidence=0.7, region=ct.regiao_batalha)
            if alvo:
                print('Atacando monstro!')
                with kills.get_lock():  # Protege a variável em ambientes com múltiplos processos
                    kills.value += 1
        except pa.ImageNotFoundException:
            pass  # Ignora se o alvo não for encontrado
        except Exception as e:
            print(f"Erro inesperado: {e}")

        if acoes.check_battle() == 'batalha':
            return

# Função para pegar loot
def pegar_loot():
    try:
        # Verifica se há loot disponível na tela
        if pa.locateOnScreen('prints/bixo_morto.png', confidence=0.45, region=ct.regiao_loot) is None:
            print("Nenhum loot encontrado.")
            return  # Sai da função se não houver loot

        # Se encontrou loot, busca todos na tela
        loot = list(pa.locateAllOnScreen('prints/bixo_morto.png', confidence=0.45, region=ct.regiao_loot))

        for box in loot:
            x, y = pa.center(box)
            pa.moveTo(x, y)
            pa.click(button='right')
            print("Pegou loot")
    except Exception as e:
        print(f"Erro ao pegar loot: {e}")

# Função para verificar o checkpoint
def checkpoint():
    return pa.locateOnScreen("prints/player_ponto.png", confidence=0.6, region=ct.regiao_mapa)

# Função para ir até a bandeira
def ir_pra_bandeira(path, esperar):
    while True:
        try:
            flag = pa.locateOnScreen(path, confidence=0.8, region=ct.regiao_mapa)
            if flag:
                if th_event.is_set():
                    return
                x, y = pa.center(flag)
                pa.moveTo(x, y)
                pa.click()
                pa.sleep(esperar)
                return
        except Exception:
            pass

# Função principal que controla as ações do bot
def run():
    with open(f'{ct.nome_pasta}/infos.json', 'r') as file:
        data = json.load(file)
        for item in data:
            if th_event.is_set():
                return
            matar_monstros()
            if th_event.is_set():
                return
            pa.sleep(1)
            pegar_loot()
            if th_event.is_set():
                return
            pa.sleep(1)
            ir_pra_bandeira(item['path'], item['esperar'])
            if th_event.is_set():
                return
            if checkpoint():
                matar_monstros()
                if th_event.is_set():
                    return
                pa.sleep(1)
                pegar_loot()
                if th_event.is_set():
                    return
                pa.sleep(1)
                ir_pra_bandeira(item['path'], item['esperar'])
                
            acoes.subir_corda(item['subir_corda'])
            if th_event.is_set():
                return
            acoes.importa_main()
            acoes.print_loot()

# Função para controlar teclas de atalho
def key_code(key, grupo_th):
    if key == keyboard.Key.esc:
        th_event.set()
        grupo_th.stop()
        print('Bot parado!')
        return False
    if key == keyboard.KeyCode.from_char("h"):
        print("Bot iniciado!")
        th_run.start()
        grupo_th.start()

# Threads para funções auxiliares
th_run = threading.Thread(target=run)

# Criando threads para vida, comida e movimento de monstro
th_life = my_thread.MyThread(acoes.acoes_game().check_vida)
th_comida = my_thread.MyThread(acoes.acoes_game().comer_comida)
th_andar_monstro = my_thread.MyThread(acoes.acoes_game().andar_monstros)

# Agrupando as threads para execução simultânea
grupo_th = my_thread.ThreadGroup([th_life, th_comida, th_andar_monstro])

# Iniciar o listener de teclas
def start():
    with Listener(on_press=lambda key: key_code(key, grupo_th)) as listener:
        listener.join()

# Inicia o bot
if __name__ == '__main__':
    manager = Manager()
    kills = manager.Value("i", 0)
    start()
    
