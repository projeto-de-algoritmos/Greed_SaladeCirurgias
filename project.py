import tkinter as tk
import tkinter.messagebox as messagebox
import re
from datetime import datetime

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
        
        tk.Label(frame_cirurgia, text="Nome do paciente:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(frame_cirurgia)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(frame_cirurgia, text="Data da Cirurgia:").grid(row=1, column=0)
        self.entry_data = tk.Entry(frame_cirurgia)
        self.entry_data.grid(row=1, column=1)
        
        tk.Label(frame_cirurgia, text="Horário de Início:").grid(row=2, column=0)
        self.entry_inicio = tk.Entry(frame_cirurgia)
        self.entry_inicio.grid(row=2, column=1)
        
        tk.Label(frame_cirurgia, text="Horário de Término:").grid(row=3, column=0)
        self.entry_termino = tk.Entry(frame_cirurgia)
        self.entry_termino.grid(row=3, column=1)
        
        tk.Button(frame_cirurgia, text="Agendar", command=self.agendar_cirurgia).grid(row=4, column=0, columnspan=2)

        frame_salas_cirurgias = tk.Frame(self)
        frame_salas_cirurgias.pack(padx=10, pady=10)

        self.text_salas = tk.Text(frame_salas_cirurgias, width=50, height=10)
        self.text_salas.pack(side=tk.LEFT)

        self.text_cirurgias = tk.Text(frame_salas_cirurgias, width=50, height=10)
        self.text_cirurgias.pack(side=tk.LEFT)



        
    def agendar_cirurgia(self):
        nome = self.entry_nome.get()
        data = self.entry_data.get()
        inicio = self.entry_inicio.get()
        termino = self.entry_termino.get()
        
        if self.verificar_data(data) and self.verificar_horario(inicio) and self.verificar_horario(termino) and self.verificar_nome(nome):
            cirurgia = (data, inicio, termino, nome)
            self.cirurgias.append(cirurgia)
            self.entry_nome.delete(0, tk.END)
            self.entry_data.delete(0, tk.END)
            self.entry_inicio.delete(0, tk.END)
            self.entry_termino.delete(0, tk.END)
            
            self.atualizar_salas_cirurgias()
        else:
            tk.messagebox.showerror("Erro", "Insira um nome, uma data (dd/mm/aaaa) e horários válidos (hh:mm).")
            
    def verificar_nome(self, nome):
        if re.match(r"^[a-zA-Z]+$", nome):
            return True
        return False

    def verificar_data(self, data):
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    def verificar_horario(self, horario):
        if re.match(r"\d{1,2}:\d{2}", horario):
            horas, minutos = map(int, horario.split(':'))
            if 0 <= horas <= 23 and 0 <= minutos <= 59:
                return True
        return False

    def atualizar_salas_cirurgias(self):
        self.text_salas.delete(1.0, tk.END)
        self.text_cirurgias.delete(1.0, tk.END)

        self.salas, _ = self.interval_partitioning(self.cirurgias)

        for i, sala in enumerate(self.salas):
            self.text_salas.insert(tk.END, f"Sala de Cirurgia {i+1}:\n")
            for cirurgia in sala:
                self.text_salas.insert(tk.END, f"\tData: {cirurgia[0]}\n\t\tPaciente: {cirurgia[3]} \n\t\tInício: {cirurgia[1]} - Término: {cirurgia[2]}\n\n")
            self.text_salas.insert(tk.END, "\n")


        cirurgia_ordenada = sorted(self.cirurgias, key=lambda x: (x[0], x[1]))

        for i, cirurgia in enumerate(cirurgia_ordenada):
            self.text_cirurgias.insert(tk.END, f"Cirurgia {i+1}:\n")
            self.text_cirurgias.insert(tk.END, f"Data: {cirurgia[0]}\n\tPaciente: {cirurgia[3]}\n\tInício: {cirurgia[1]} - Término: {cirurgia[2]}\n\n")

    def interval_partitioning(self, cirurgias):
        cirurgias_ordenadas = sorted(cirurgias, key=lambda x: (x[0], x[1]))
        salas = []

        for cirurgia in cirurgias_ordenadas:
            alocado = False
            for sala in salas:
                if cirurgia[0] != sala[-1][0]:
                    sala.append(cirurgia)
                    alocado = True
                    break
                elif cirurgia[0] == sala[-1][0]:
                    if cirurgia[1] >= sala[-1][2]:
                        sala.append(cirurgia)
                        alocado = True
                        break


            if not alocado:
                salas.append([cirurgia])

        return salas, cirurgias_ordenadas

if __name__ == "__main__":
    app = Application()
    app.mainloop()
