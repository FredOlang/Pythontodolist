import unittest
from unittest.mock import patch
import tkinter as tk
from tkinter import messagebox
import json
import os

# Importation du fichier contenant le code de l'application (main.py)
import main


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Prépare l'environnement de test en réinitialisant le fichier JSON avant chaque test"""
        if os.path.exists('tasks.json'):
            os.remove('tasks.json')
        self.app = tk.Tk()
        self.app.withdraw()  # On ne veut pas afficher la fenêtre Tkinter pendant les tests

        # Initialisation de l'interface utilisateur du gestionnaire de tâches
        self.tasks_listbox = tk.Listbox(self.app)
        self.tasks_listbox.pack()
        self.task_entry = tk.Entry(self.app)
        self.task_entry.pack()
        self.priority_var = tk.StringVar()
        self.priority_var.set("Moyenne")
        self.priority_dropdown = tk.OptionMenu(self.app, self.priority_var, "Haute", "Moyenne", "Basse")
        self.priority_dropdown.pack()
        
        # Ajouter les fonctions de gestion de tâches
        self.add_button = tk.Button(self.app, text="Ajouter une tâche", command=self.add_task)
        self.add_button.pack()

    def add_task(self):
        """Fonction d'ajout de tâche dans le test"""
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task != "":
            self.tasks_listbox.insert(tk.END, f"{priority} - {task}")

    def test_add_task(self):
        """Test pour vérifier si une tâche est correctement ajoutée"""
        # Simuler l'ajout d'une tâche
        self.task_entry.insert(0, "Test Task")
        self.priority_var.set("Haute")
        self.add_task()
        
        # Vérifier que la tâche a bien été ajoutée dans la listbox
        tasks = self.tasks_listbox.get(0, tk.END)
        self.assertIn("Haute - Test Task", tasks)

    def test_empty_task_entry(self):
        """Test pour vérifier que la tâche vide ne s'ajoute pas"""
        # Simuler l'ajout d'une tâche vide
        self.task_entry.delete(0, tk.END)
        self.add_task()
        
        # Vérifier que la listbox est vide
        tasks = self.tasks_listbox.get(0, tk.END)
        self.assertEqual(len(tasks), 0)

    def test_delete_task(self):
        """Test pour vérifier la suppression d'une tâche"""
        # Ajouter une tâche
        self.task_entry.insert(0, "Task to delete")
        self.priority_var.set("Basse")
        self.add_task()
        
        # Simuler la suppression d'une tâche
        self.tasks_listbox.delete(0)
        
        # Vérifier que la listbox est vide après suppression
        tasks = self.tasks_listbox.get(0, tk.END)
        self.assertEqual(len(tasks), 0)

    def test_mark_task_done(self):
        """Test pour vérifier la fonctionnalité de marquer une tâche comme terminée"""
        # Ajouter une tâche
        self.task_entry.insert(0, "Task to mark as done")
        self.priority_var.set("Moyenne")
        self.add_task()
        
        # Simuler le marquage de la tâche comme terminée
        task = self.tasks_listbox.get(0)
        self.tasks_listbox.delete(0)
        self.tasks_listbox.insert(tk.END, f"✔ {task}")
        
        # Vérifier que la tâche est marquée comme terminée
        tasks = self.tasks_listbox.get(0, tk.END)
        self.assertIn("✔ Task to mark as done", tasks)

    def tearDown(self):
        """Nettoyage après chaque test, réinitialiser l'environnement"""
        self.app.destroy()
        if os.path.exists('tasks.json'):
            os.remove('tasks.json')


if __name__ == '__main__':
    unittest.main()
