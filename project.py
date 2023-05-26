import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agendamento de Cirurgias")
        
        self.cirurgias = []
        self.salas = []
        
        self.create_widgets()
    
    def create_widgets(self):
        frame_cirurgia = tk.Frame(self)
        frame_cirurgia.pack(padx=10, pady=10)
        
        tk.Label(frame_cirurgia, text="Horário de Início:").grid(row=0, column=0)
        self.entry_inicio = tk.Entry(frame_cirurgia)
        self.entry_inicio.grid(row=0, column=1)
        
        tk.Label(frame_cirurgia, text="Horário de Término:").grid(row=1, column=0)
        self.entry_termino = tk.Entry(frame_cirurgia)
        self.entry_termino.grid(row=1, column=1)
        
        tk.Button(frame_cirurgia, text="Agendar", command=self.agendar_cirurgia).grid(row=2, column=0, columnspan=2)
        
        frame_salas_cirurgias = tk.Frame(self)
        frame_salas_cirurgias.pack(padx=10, pady=10)
        
        self.text_salas = tk.Text(frame_salas_cirurgias, width=30, height=10)
        self.text_salas.pack(side=tk.LEFT)
        
        self.text_cirurgias = tk.Text(frame_salas_cirurgias, width=30, height=10)
        self.text_cirurgias.pack(side=tk.LEFT)
        
    def agendar_cirurgia(self):
        inicio = self.entry_inicio.get()
        termino = self.entry_termino.get()
        
        if inicio and termino:
            cirurgia = (inicio, termino)
            self.cirurgias.append(cirurgia)
            self.entry_inicio.delete(0, tk.END)
            self.entry_termino.delete(0, tk.END)
            
            self.atualizar_salas_cirurgias()
        
    def atualizar_salas_cirurgias(self):
        self.text_salas.delete(1.0, tk.END)
        self.text_cirurgias.delete(1.0, tk.END)
        
        self.salas, _ = self.interval_partitioning(self.cirurgias)
        
        for i, sala in enumerate(self.salas):
            self.text_salas.insert(tk.END, f"Sala {i+1}:\n")
            for cirurgia in sala:
                self.text_salas.insert(tk.END, f"Início: {cirurgia[0]} - Término: {cirurgia[1]}\n")
            self.text_salas.insert(tk.END, "\n")
        
        for cirurgia in self.cirurgias:
            self.text_cirurgias.insert(tk.END, f"Início: {cirurgia[0]} - Término: {cirurgia[1]}\n")
    
    def interval_partitioning(self, cirurgias):
        cirurgias_ordenadas = sorted(cirurgias, key=lambda x: x[0])
        salas = []
        
        for cirurgia in cirurgias_ordenadas:
            alocado = False
            for sala in salas:
                if cirurgia[0] >= sala[-1][1]:
                    sala.append(cirurgia)
                    alocado = True
                    break
            
            if not alocado:
                salas.append([cirurgia])
        
        return salas, cirurgias_ordenadas
    
if __name__ == "__main__":
    app = Application()
    app.mainloop()
