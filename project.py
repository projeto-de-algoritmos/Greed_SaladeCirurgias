import tkinter as tk
from tkinter import messagebox

class Materia:
    def __init__(self, nome, horario_inicio, horario_fim):
        self.nome = nome
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim

class App:
    def __init__(self, root):
        self.materias = []
        self.root = root
        self.root.title("Seletor de Matérias")
        # Labels e campos de entrada
        self.label_nome = tk.Label(root, text="Nome da Matéria:")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(root)
        self.entry_nome.pack()
    
        self.label_inicio = tk.Label(root, text="Horário de Início:")
        self.label_inicio.pack()
        self.entry_inicio = tk.Entry(root)
        self.entry_inicio.pack()
        
        self.label_fim = tk.Label(root, text="Horário de Fim:")
        self.label_fim.pack()
        self.entry_fim = tk.Entry(root)
        self.entry_fim.pack()
        
        # Botão "Adicionar"
        self.button_adicionar = tk.Button(root, text="Adicionar", command=self.adicionar_materia)
        self.button_adicionar.pack()
        
        # Lista de matérias adicionadas
        self.lista_materias = tk.Listbox(root)
        self.lista_materias.pack()
        
        # Botão "Montar Grade"
        self.button_grade = tk.Button(root, text="Montar Grade", command=self.montar_grade)
        self.button_grade.pack()
    
    def adicionar_materia(self):
        nome = self.entry_nome.get()
        inicio = self.entry_inicio.get()
        fim = self.entry_fim.get()
        
        if nome and inicio and fim:
            materia = Materia(nome, inicio, fim)
            self.materias.append(materia)
            
            self.lista_materias.insert(tk.END, f"{materia.nome} - Início: {materia.horario_inicio} / Fim: {materia.horario_fim}")
            
            self.entry_nome.delete(0, tk.END)
            self.entry_inicio.delete(0, tk.END)
            self.entry_fim.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
    
    def montar_grade(self):
     if len(self.materias) > 0:
        # Ordena as matérias pelo horário de fim
        self.materias.sort(key=lambda x: x.horario_fim)
        
        grades = [[]]  # Lista de grades
        grades[0].append(self.materias[0])  # Adiciona a primeira matéria à primeira grade
        
        # Percorre as matérias restantes
        for i in range(1, len(self.materias)):
            inserido = False
            
            # Verifica em qual grade é possível inserir a matéria
            for j in range(len(grades)):
                if self.materias[i].horario_inicio >= grades[j][-1].horario_fim:
                    grades[j].append(self.materias[i])
                    inserido = True
                    break
            
            # Se não for possível inserir em nenhuma grade existente, cria uma nova grade
            if not inserido:
                grades.append([self.materias[i]])
        
        # Exibe as grades resultantes
        messagebox.showinfo("Montar Grade", "Grade montada com sucesso!\n\nGrades Resultantes:\n" + self.formatar_grades(grades))
     else:
        messagebox.showerror("Erro", "Adicione pelo menos uma matéria antes de montar a grade.")

def formatar_grades(self, grades):
    resultado = ""
    for i, grade in enumerate(grades):
        resultado += f"Grade {i+1}:\n"
        for materia in grade:
            resultado += f"{materia.nome} - Início: {materia.horario_inicio} / Fim: {materia.horario_fim}\n"
        resultado += "\n"
    return resultado

        

root = tk.Tk()
app = App(root)
root.mainloop()
