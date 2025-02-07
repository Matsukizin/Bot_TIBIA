import pyautogui as pa
import constants as ct
import main
import pytesseract
import cv2
import re
import numpy as np
import json
import os

def importa_main():
    from main import kills
    print_loot()

class acoes_game():
    def __init__(self):
        print('oii')
        self.count = 0
        self.infos = {}
        self.regiao_player = ct.regiao_loot
        
    def subir_corda(deveria_subir):
        if deveria_subir:
            achar_ancora = pa.locateOnScreen("prints/ancora.png", confidence=0.4, region=ct.regiao_loot)
            if achar_ancora:
                x, y = pa.center(achar_ancora)
                pa.moveTo(x - 40, y + 40)
                pa.press("F7")
                pa.click()


    def comer_comida():
        while True:
            comidas = [5]  # Lista de comidas a serem consumidas
            for comida in comidas:
                pa.press("F6")
                print("Comendo food...")
                pa.sleep(1)
            pa.sleep(1200 - 30)


    def check_vida():
        print("Checando vida...")
        while True:
            pa.sleep(ct.delay)
            if pa.pixelMatchesColor(ct.vida_x, ct.vida_y, ct.vida_rgb):
                print("Vida baixa! Curando...")
                pa.press(ct.nome_botao)
            elif pa.pixelMatchesColor(ct.vida_x, ct.vida_y, ct.vida_rgb):  # Corrigido o check
                print("Vida cheia")
                break

            pa.sleep(32)


    def check_battle():
        try:
            batalha = pa.locateOnScreen('prints/lista_batalha.png', region=ct.regiao_batalha)
            return batalha
        except Exception:
            return None


    def andar_monstros():
        while True:
            box = pa.locateOnScreen('prints/andar_monstro.png', confidence=0.8, region=ct.regiao_andar_monstro)
            if box:
                pass
            elif pa.center(ct.regiao_andar_monstro):
                pa.click()

            pa.sleep(30)

    def ir_pra_bandeira(self, path, esperar):
        while True:
            try:
                flag = pa.locateOnScreen(path, confidence=0.6, region=ct.regiao_mapa)
                if flag:
                    x, y = pa.center(flag)
                    pa.moveTo(x, y)
                    pa.click()
                    pa.sleep(esperar)
                    return
            except Exception:
                pass

    def vender(self):
        pa.locateOnScreen("prints/Menu_geral", confidence=0.8, region=self.regiao_player)
        pa.click()
        pa.sleep(1)
        pa.locateOnScreen("prints/depot_menu.png", confidence=0.6)
        pa.click()
        pa.sleep(1)
        pa.locateOnScreen("prints/depot_2.png", confidence=0.6)
        pa.click()
        pa.sleep(1)
        x1, y1 = pa.locateOnScreen("prints/medicines.png", confidence=0.5)
        x2, y2 = pa.locateOnScreen("prints/slots.png", confidence=0.8)
        pa.moveTo(x1, y1)
        pa.mouseDown()
        pa.sleep(1)
        pa.moveTo(x2, y2, 1)
        pa.mouseUp()
        pa.sleep(0.5)
        pa.locateOnScreen("prints/X.png", confidence=0.8)
        pa.click()
        pa.sleep(0.5)
        pa.locateOnScreen("prints/Menu_geral", confidence=0.8, region=self.regiao_player)
        pa.click()
        pa.sleep(0.5)
        pa.locateOnScreen("prints/menu_venda.png", confidence=1)
        pa.sleep(1)
        pa.write("medicine", 1)
        pa.sleep(1)
        pa.locateOnScreen("prints/select_medicine.png", confidence=0.4)
        pa.click()
        pa.screenshot(region=ct.regiao_medicine)
        path = f"{ct.pasta_medicines}/Medicines_{self.count}.png"
        pa.save(path)

    def voltar_venda(self):
        with open(f'{ct.voltar_venda}/infos.json', 'r') as file:
            data = json.load(file)
            for item in data:
                self.ir_pra_bandeira(item['path'], item['esperar'])
                self.verificar()
                if self.verificar():
                    self.ir_pra_bandeira(item['path'], item['esperar'])

    def verificar(self):
        return pa.locateOnScreen("prints/player_ponto.png", confidence=0.6, region=self.regiao_mapa)

    def run(self):
        with open(f'{ct.vender_caminho}/infos.json', 'r') as file:
            data = json.load(file)
            if main.pause == 1:
                main.th_event.set()
                main.grupo_th.stop()
                print('Bot parado para vender itens')
                pa.sleep(1)
                for item in data:
                    self.ir_pra_bandeira(item['path'], item['esperar'])
                    self.verificar()
                    if self.verificar():
                        self.ir_pra_bandeira(item['path'], item['esperar'])
                try:
                    self.vender()
                    self.voltar_venda()
                    pa.sleep(30)
                    pause = 0
                    pa.write("h")
                except Exception as e:
                    print(f"Ocorreu um erro ao vender: {e}")


def print_loot():
    x, y = ct.regiao_mochila
    global pause
    taxa = 10
    Resets = 0
    prints = 0

    if kills >= taxa:
        taxa += 10
        detalhes = []

        foto = pa.screenshot(region=(x - 8, y - 8, 16, 16))
        path = f"{ct.pasta_mochila}/mochila_{prints}.png"
        foto.save(path)
        prints += 1

        infos = {
            "medicine": 0,
            "packs de gold": 0,
            "ta cheio?": "Não",
            "Kills até o momento": kills,
            "Prints até o momento": prints,
            "Resets": Resets
        }
        detalhes.append(infos)

        detalhes_path = f"{ct.pasta_mochila}/detalhes_{prints}.json"
        with open(detalhes_path, "w") as file:
            json.dump(detalhes, file, indent=4)

        if kills >= 1000:
            reset_path = f"{ct.pasta_mochila}/reset_{Resets + 1}.json"
            os.rename(detalhes_path, reset_path)

            reset_img_path = f"{ct.pasta_mochila}/reset_{Resets + 1}.png"
            os.rename(path, reset_img_path)

            for file in os.listdir(ct.pasta_mochila):
                if file.startswith("mochila_") and file.endswith(".png"):
                    os.remove(os.path.join(ct.pasta_mochila, file))

            for file in os.listdir(ct.pasta_mochila):
                if file.startswith("detalhes_") and file.endswith(".json"):
                    os.remove(os.path.join(ct.pasta_mochila, file))

            Resets += 1
            taxa = 10
            pause = 1

            self.run()
