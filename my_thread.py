import threading

class MyThread():
    def __init__(self, work):
        self.event = threading.Event()
        self.work = work
        self.thread = threading.Thread(target=self.run)  # Atribuindo a função run ao thread
        
    def start(self):
        self.event.clear()
        self.thread = threading.Thread(target=self.run)  # Inicializando o thread
        self.thread.start()
        
    def stop(self):
        self.event.set()   # Define o evento como setado, interrompendo o loop no 'run'
        self.thread.join()  # Aguarda o término do thread
        
    def run(self):
        while not self.event.is_set():
            self.work()  # Chama a função work, não apenas referencia

class ThreadGroup:
    def __init__(self, lista_thread):
        self.my_threads = lista_thread
        
    def start(self):
        for thread in self.my_threads:
            thread.start()
            
    def stop(self):
        for thread in self.my_threads:
            thread.stop()
