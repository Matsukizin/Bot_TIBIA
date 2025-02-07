import pyautogui as pa
from pynput.keyboard import Listener
from pynput import keyboard
import os
import json
import constants as ct


def criar_pasta():
    if not os.path.isdir(ct.nome_pasta):
        os.mkdir(ct.nome_pasta)
        print("Pasta criada!")
    else:
        print("Pasta já criada!")


class rec:
    def __init__(self):
        criar_pasta()
        print("oi")
        self.count = 0
        self.coordinates = []

    def foto(self):
        x, y = pa.position()
        foto = pa.screenshot(region=(x - 8, y - 8, 16, 16))
        path = f"{ct.nome_pasta}/bandeira_{self.count}.png"
        foto.save(path)
        self.count += 1
        infos = {
            "path": path,
            "descer_escada": 0,
            "subir_corda": 0,
            "esperar": 15  # Corrigido erro de sintaxe
        }
        self.coordinates.append(infos)

    def descer_escada(self):
        if self.coordinates:  # Verifica se a lista não está vazia
            last_coordinates = self.coordinates[-1]
            last_coordinates["descer_escada"] = 1
        else:
            print("Erro: Nenhuma coordenada registrada para descer a escada!")

    def subir_corda(self):
        if self.coordinates:  # Verifica se a lista não está vazia
            last_coordinates = self.coordinates[-1]
            last_coordinates["subir_corda"] = 1  # Corrigido nome da chave
        else:
            print("Erro: Nenhuma coordenada registrada para subir a corda!")

    def key_code(self, key):
        if key == keyboard.Key.esc:
            with open(f"{ct.nome_pasta}/infos.json", "w") as file:
                json.dump(self.coordinates, file, indent=4)  # Corrigido json.dump
            return False

        if key == keyboard.KeyCode.from_char("h"):  # Corrigido erro de comparação com string
            self.foto()

        if key == keyboard.Key.page_down:
            self.descer_escada()

        if key == keyboard.Key.page_up:
            self.subir_corda()

    def start(self):
        with Listener(on_press=self.key_code) as listener:
            listener.join()


record = rec()
record.start()
