import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agendamento de Salas de Reunião")
        
        self.reunioes = []
        self.salas = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame para adicionar uma nova reunião
        frame_reuniao = tk.Frame(self)
        frame_reuniao.pack(padx=10, pady=10)
        
        tk.Label(frame_reuniao, text="Horário de Início:").grid(row=0, column=0)
        self.entry_inicio = tk.Entry(frame_reuniao)
        self.entry_inicio.grid(row=0, column=1)
        
        tk.Label(frame_reuniao, text="Horário de Término:").grid(row=1, column=0)
        self.entry_termino = tk.Entry(frame_reuniao)
        self.entry_termino.grid(row=1, column=1)
        
        tk.Button(frame_reuniao, text="Agendar", command=self.agendar_reuniao).grid(row=2, column=0, columnspan=2)
        
        # Frame para exibir as salas e reuniões agendadas
        frame_salas_reunioes = tk.Frame(self)
        frame_salas_reunioes.pack(padx=10, pady=10)
        
        self.text_salas = tk.Text(frame_salas_reunioes, width=30, height=10)
        self.text_salas.pack(side=tk.LEFT)
        
        self.text_reunioes = tk.Text(frame_salas_reunioes, width=30, height=10)
        self.text_reunioes.pack(side=tk.LEFT)
        
    def agendar_reuniao(self):
        inicio = self.entry_inicio.get()
        termino = self.entry_termino.get()
        
        if inicio and termino:
            reuniao = (inicio, termino)
            self.reunioes.append(reuniao)
            self.entry_inicio.delete(0, tk.END)
            self.entry_termino.delete(0, tk.END)
            
            self.atualizar_salas_reunioes()
        
    def atualizar_salas_reunioes(self):
        # Limpa os textos das salas e reuniões
        self.text_salas.delete(1.0, tk.END)
        self.text_reunioes.delete(1.0, tk.END)
        
        # Realiza o agendamento das reuniões
        self.salas, _ = self.interval_partitioning(self.reunioes)
        
        # Atualiza o texto das salas
        for i, sala in enumerate(self.salas):
            self.text_salas.insert(tk.END, f"Sala {i+1}:\n")
            for reuniao in sala:
                self.text_salas.insert(tk.END, f"Início: {reuniao[0]} - Término: {reuniao[1]}\n")
            self.text_salas.insert(tk.END, "\n")
        
        # Atualiza o texto das reuniões
        for reuniao in self.reunioes:
            self.text_reunioes.insert(tk.END, f"Início: {reuniao[0]} - Término: {reuniao[1]}\n")
    
    def interval_partitioning(self, reunioes):
        reunioes_ordenadas = sorted(reunioes, key=lambda x: x[0])
        salas = []
        
        for reuniao in reunioes_ordenadas:
            alocado = False
            for sala in salas:
                if reuniao[0] >= sala[-1][1]:
                    sala.append(reuniao)
                    alocado = True
                    break
            
            if not alocado:
                salas.append([reuniao])
        
        return salas, reunioes_ordenadas
    
if __name__ == "__main__":
    app = Application()
    app.mainloop()
