import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# Fonction pour ajouter une tâche
def add_task():
    task = task_entry.get()
    priority = priority_var.get()
    if task != "":
        tasks_listbox.insert(tk.END, f"{priority} - {task}")
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Entrée vide", "Veuillez entrer une tâche.")

# Fonction pour supprimer une tâche sélectionnée
def delete_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        tasks_listbox.delete(selected_task_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Aucune tâche sélectionnée", "Veuillez sélectionner une tâche à supprimer.")

# Fonction pour marquer une tâche comme terminée
def mark_as_done():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        task = tasks_listbox.get(selected_task_index)
        tasks_listbox.delete(selected_task_index)
        tasks_listbox.insert(tk.END, f"✔ {task}")
        save_tasks()
    except IndexError:
        messagebox.showwarning("Aucune tâche sélectionnée", "Veuillez sélectionner une tâche à marquer comme terminée.")

# Fonction pour modifier une tâche sélectionnée
def edit_task():
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        old_task = tasks_listbox.get(selected_task_index)
        new_task = task_entry.get()
        if new_task != "":
            tasks_listbox.delete(selected_task_index)
            priority = priority_var.get()
            tasks_listbox.insert(tk.END, f"{priority} - {new_task}")
            save_tasks()
        else:
            messagebox.showwarning("Entrée vide", "Veuillez entrer un nouveau texte pour la tâche.")
    except IndexError:
        messagebox.showwarning("Aucune tâche sélectionnée", "Veuillez sélectionner une tâche à modifier.")

# Fonction pour sauvegarder les tâches dans un fichier JSON
def save_tasks():
    tasks = tasks_listbox.get(0, tk.END)
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

# Fonction pour charger les tâches depuis le fichier JSON
def load_tasks():
    if os.path.exists('tasks.json'):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
                for task in tasks:
                    tasks_listbox.insert(tk.END, task)
        except json.JSONDecodeError:
            messagebox.showerror("Erreur de fichier", "Le fichier de tâches est corrompu.")
    else:
        pass  # Si le fichier n'existe pas, on ignore l'erreur

# Création de la fenêtre principale
app = tk.Tk()
app.title("Gestionnaire de Tâches")

# Création de l'interface utilisateur
frame = tk.Frame(app)
frame.pack(pady=20)

task_entry = tk.Entry(frame, width=50)
task_entry.grid(row=0, column=0, padx=10)

# Variable de priorité avec une liste déroulante
priority_var = tk.StringVar()
priority_var.set("Moyenne")
priority_dropdown = ttk.Combobox(frame, textvariable=priority_var, values=["Haute", "Moyenne", "Basse"])
priority_dropdown.grid(row=0, column=1, padx=10)

add_button = ttk.Button(frame, text="Ajouter une tâche", command=add_task)
add_button.grid(row=0, column=2, padx=10)

tasks_listbox = tk.Listbox(app, width=80, height=10)
tasks_listbox.pack(pady=10)

mark_done_button = ttk.Button(app, text="Marquer comme terminée", command=mark_as_done)
mark_done_button.pack(pady=5)

edit_button = ttk.Button(app, text="Modifier la tâche", command=edit_task)
edit_button.pack(pady=5)

delete_button = ttk.Button(app, text="Supprimer une tâche", command=delete_task)
delete_button.pack(pady=5)

# Charger les tâches au démarrage de l'application
load_tasks()

# Lancer l'application
app.mainloop()
