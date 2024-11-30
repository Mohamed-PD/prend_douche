import tkinter as tk  # Importation de la bibliothèque tkinter pour créer des interfaces graphiques
from tkinter import messagebox, filedialog, colorchooser  # Importation de modules spécifiques pour les boîtes de dialogue

class Application(tk.Tk):  # Définition de la classe Application qui hérite de tk.Tk
    def __init__(self):  # Constructeur de la classe
        super().__init__()  # Appelle le constructeur de la classe parente
        self.title("Mon Application")  # Définit le titre de la fenêtre
        self.geometry("800x600")  # Définit la taille de la fenêtre
       
        self.canvas = tk.Canvas(self, bg='white')  # Création d'un canevas blanc pour dessiner
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Le canevas s'étend pour remplir la fenêtre

        self.create_menu()  # Appel à la méthode pour créer le menu

        self.vertices = {}  # Dictionnaire pour stocker les sommets
        self.edges = []  # Liste pour stocker les arêtes
        self.vertex_count = 1  # Compteur de sommets
        self.selected_vertices = []  # Liste des sommets sélectionnés
        self.add_vertex_mode = False  # Mode d'ajout de sommets
        self.connect_mode = False  # Mode de connexion des sommets
        
        # Piles pour gérer les actions
        self.undo_stack = []  # Pile pour gérer les actions pour l'annulation

    def create_menu(self):  # Méthode pour créer le menu
        menu_bar = tk.Menu(self)  # Création de la barre de menu

        # Menu Fichier
        file_menu = tk.Menu(menu_bar, tearoff=0)  # Création d'un sous-menu "Fichier"
        file_menu.add_command(label="Nouveau", command=self.open_new_window)  # Commande pour ouvrir une nouvelle fenêtre
        file_menu.add_command(label="Ouvrir", command=self.open_file)  # Commande pour ouvrir un fichier
        file_menu.add_command(label="Enregistre sous", command=self.save_file)  # Commande pour sauvegarder
        file_menu.add_separator()  # Séparateur dans le menu
        file_menu.add_command(label="Quitter", command=self.quit)  # Commande pour quitter l'application
        menu_bar.add_cascade(label="Fichier", menu=file_menu)  # Ajout du menu "Fichier" à la barre de menu

        # Menu Création
        graph_menu = tk.Menu(menu_bar, tearoff=0)  # Sous-menu "Graphe"
        graph_menu.add_command(label="Sommet", command=self.activate_vertex_mode)  # Commande pour activer le mode ajout de sommet
        graph_menu.add_command(label="Arrêter", command=self.activate_connect_mode)  # Commande pour activer le mode connexion
        
        creation_menu = tk.Menu(menu_bar, tearoff=0)  # Sous-menu "Création"
        creation_menu.add_cascade(label="Graphe", menu=graph_menu)  # Ajout du menu "Graphe"
        menu_bar.add_cascade(label="Création", menu=creation_menu)  # Ajout du menu "Création"

        # Menu Éditeur
        editor_menu = tk.Menu(menu_bar, tearoff=0)  # Sous-menu "Éditeur"
        editor_menu.add_command(label="graphe", command=self.undo)  # Commande pour annuler une action
        menu_bar.add_cascade(label="Éditeur", menu=editor_menu)  # Ajout du menu "Éditeur"

        # Menu Affichage
        display_menu = tk.Menu(menu_bar, tearoff=0)  # Sous-menu "Affichage"
        display_menu.add_command(label="graphe", command=self.open_zoom_window)  # Commande pour afficher le graphe
        display_menu.add_command(label="chaine", command=self.preview)  # Commande pour un aperçu (non implémenté)
        display_menu.add_command(label="matrices", command=self.display)  # Commande pour afficher les matrices (non implémenté)
        menu_bar.add_cascade(label="Affichage", menu=display_menu)  # Ajout du menu "Affichage"
        
        # Menu Exécution
        execution_menu = tk.Menu(menu_bar, tearoff=0)  # Sous-menu "Exécution"
        execution_menu.add_command(label="plus cour chemin", command=self.open_zoom_window)  # Commande pour un chemin plus court
        execution_menu.add_command(label="coloration", command=self.preview)  # Commande pour la coloration (non implémenté)
        menu_bar.add_cascade(label="Execution", menu=execution_menu)  # Ajout du menu "Exécution"

        # Menu Aide
        help_menu = tk.Menu(menu_bar, tearoff=0)  # Sous-menu "Aide"
        help_menu.add_command(label="À propos", command=self.about)  # Commande pour afficher des informations sur l'application
        menu_bar.add_cascade(label="Aide", menu=help_menu)  # Ajout du menu "Aide"

        self.config(menu=menu_bar)  # Configuration de la fenêtre avec la barre de menu

        # Liaisons d'événements pour le canevas
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # gérer les actions
        self.canvas.bind("<Button-3>", self.select_vertex)  # sélectionner un sommet

    def open_new_window(self):  # Méthode pour ouvrir une nouvelle fenêtre
        new_window = Application()  # Création d'une nouvelle instance de l'application
        new_window.title("Nouvelle Fenêtre")  # Titre de la nouvelle fenêtre
        new_window.geometry("400x300")  # Taille de la nouvelle fenêtre
        new_window.mainloop()  # Démarrage de la boucle principale de la nouvelle fenêtre

    def open_file(self):  # Méthode pour ouvrir un fichier
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.*")])  # Sélecteur de fichier
        if file_path:  # Si un fichier a été sélectionné
            try:
                with open(file_path, 'r') as file:  # Ouverture du fichier en mode lecture
                    new_window = Application()  # Création d'une nouvelle instance de l'application
                    new_window.title("Fichier Ouvert")  # Titre de la nouvelle fenêtre
                    new_window.geometry("400x300")  # Taille de la nouvelle fenêtre

                    for line in file:  # Pour chaque ligne du fichier
                        if line.startswith("edge"):  # Si la ligne commence par "edge"
                            _, x1, y1, x2, y2 = line.strip().split(',')  # Décomposition des coordonnées
                            new_window.canvas.create_line(int(x1), int(y1), int(x2), int(y2), fill='red', width=2)  # Dessine l'arête
                            new_window.edges.append(((int(x1), int(y1)), (int(x2), int(y2))))  # Ajoute l'arête à la liste
                        else:  # Pour les sommets
                            vertex_id, x, y = map(int, line.strip().split(','))  # Décomposition des coordonnées du sommet
                            new_window.vertices[vertex_id] = (x, y)  # Ajoute le sommet au dictionnaire
                            new_window.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')  # Dessine le sommet
                            new_window.canvas.create_text(x, y - 10, text=str(vertex_id), fill='black')  # Étiquette pour le sommet
                            new_window.vertex_count = max(new_window.vertex_count, vertex_id + 1)  # Met à jour le compteur de sommets

                    new_window.mainloop()  # Démarre la boucle principale de la nouvelle fenêtre
                    messagebox.showinfo("Fichier Ouvrir", f"Fichier chargé : {file_path}")  # Message d'information sur le chargement
            except Exception as e:  # En cas d'erreur
                messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du fichier : {e}")  # Message d'erreur

    def save_file(self):  # Méthode pour sauvegarder un fichier
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])  # Sélecteur de sauvegarde
        if file_path:  # Si un chemin de fichier a été sélectionné
            try:
                with open(file_path, 'w') as file:  # Ouverture du fichier en mode écriture
                    for vertex_id, (x, y) in self.vertices.items():  # Pour chaque sommet
                        file.write(f"{vertex_id},{x},{y}\n")  # Écriture des coordonnées du sommet
                    for edge in self.edges:  # Pour chaque arête
                        file.write(f"edge,{edge[0][0]},{edge[0][1]},{edge[1][0]},{edge[1][1]}\n")  # Écriture des coordonnées de l'arête
                messagebox.showinfo("Sauvegarder", "Fichier sauvegardé avec succès.")  # Message de succès
            except Exception as e:  # En cas d'erreur
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde du fichier : {e}")  # Message d'erreur

    def activate_vertex_mode(self):  # Méthode pour activer le mode d'ajout de sommet
        self.add_vertex_mode = True  # Active le mode ajout de sommet
        self.connect_mode = False  # Désactive le mode de connexion
        self.selected_vertices.clear()  # Efface la sélection des sommets

    def activate_connect_mode(self):  # Méthode pour activer le mode de connexion
        self.connect_mode = True  # Active le mode de connexion
        self.add_vertex_mode = False  # Désactive le mode ajout de sommet
        self.selected_vertices.clear()  # Efface la sélection des sommets

    def on_canvas_click(self, event):  # Méthode pour gérer les clics sur le canevas
        if self.add_vertex_mode:  # Si le mode ajout de sommet est actif
            self.record_action()  # Enregistre l'action avant de modifier
            x, y = event.x, event.y  # Coordonnées de la souris
            self.vertices[self.vertex_count] = (x, y)  # Ajoute le nouveau sommet
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')  # Dessine le sommet
            self.canvas.create_text(x, y - 10, text=str(self.vertex_count), fill='white')  # Étiquette pour le sommet
            self.vertex_count += 1  # Incrémente le compteur de sommets
        elif self.connect_mode:  # Si le mode connexion est actif
            self.select_vertex(event)  # Sélectionne un sommet
            # Si deux sommets sont sélectionnés, dessine la ligne
            if len(self.selected_vertices) == 2:  # Vérifie si deux sommets sont sélectionnés
                v1 = self.selected_vertices[0]  # Premier sommet
                v2 = self.selected_vertices[1]  # Deuxième sommet
                x1, y1 = self.vertices[v1]  # Coordonnées du premier sommet
                x2, y2 = self.vertices[v2]  # Coordonnées du deuxième sommet
                self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2)  # Dessine l'arête
                self.edges.append(((x1, y1), (x2, y2)))  # Ajoute l'arête à la liste
                self.selected_vertices.clear()  # Réinitialise la sélection
        
    def select_vertex(self, event):  # Méthode pour sélectionner un sommet
        x, y = event.x, event.y  # Coordonnées de la souris
        for num, (vx, vy) in self.vertices.items():  # Pour chaque sommet
            if abs(vx - x) <= 5 and abs(vy - y) <= 5:  # Vérifie si le clic est proche du sommet
                if num not in self.selected_vertices:  # Si le sommet n'est pas déjà sélectionné
                    self.selected_vertices.append(num)  # Ajoute le sommet à la sélection
                break  # Sort de la boucle
        else:  # Si aucun sommet n'est sélectionné
            # Vérifie si une arête est sélectionnée
            for edge in self.edges:  # Pour chaque arête
                if (abs(edge[0][0] - x) <= 5 and abs(edge[0][1] - y) <= 5) or \
                   (abs(edge[1][0] - x) <= 5 and abs(edge[1][1] - y) <= 5):  # Vérifie si le clic est proche d'une extrémité
                    # Sélectionne l'arête
                    self.selected_vertices = [edge]  # Ajoute l'arête à la sélection
                    break  # Sort de la boucle

    def redraw_canvas(self):  # Méthode pour redessiner le canevas
        self.canvas.delete("all")  # Efface tout sur le canevas
        for vertex_id, (x, y) in self.vertices.items():  # Pour chaque sommet
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')  # Dessine le sommet
            self.canvas.create_text(x, y - 10, text=str(vertex_id), fill='black')  # Étiquette pour le sommet
        for edge in self.edges:  # Pour chaque arête
            self.canvas.create_line(edge[0], edge[1], fill='red', width=2)  # Dessine l'arête

    def record_action(self):  # Méthode pour enregistrer l'état actuel
        self.undo_stack.append((self.vertices.copy(), self.edges.copy()))  # Ajoute l'état actuel à la pile d'annulation

    def undo(self):  # Méthode pour annuler la dernière action
        messagebox.showinfo("Copier", "Sommets copiés dans le presse-papiers.")  # Message de confirmation

    def copy(self):  # Méthode pour copier des sommets
        messagebox.showinfo("Copier", "Sommets copiés dans le presse-papiers.")  # Message de confirmation

    def paste(self):  # Méthode pour coller des sommets
         messagebox.showinfo("Copier", "Sommets copiés dans le presse-papiers.")  # Message de confirmation

    def zoom_in(self):  # Méthode pour zoomer avant
        messagebox.showinfo("Copier", "Sommets copiés dans le presse-papiers.")  # Message de confirmation

    def zoom_out(self):  # Méthode pour zoomer arrière
         messagebox.showinfo("Copier", "Sommets copiés dans le presse-papiers.")  # Message de confirmation

    def preview(self):  # Méthode pour l'aperçu (non implémenté)
        messagebox.showinfo("Aperçu", "Fonctionnalité Aperçu à implémenter.")  # Message d'information

    def display(self):  # Méthode pour afficher des données (non implémenté)
        messagebox.showinfo("Affichage", "Fonctionnalité Affichage à implémenter.")  # Message d'information

    def about(self):  # Méthode pour afficher des informations sur l'application
        messagebox.showinfo("À propos", "Mon Application Graphe v1.0\nDéveloppé avec Tkinter")  # Affichage des informations

    def open_zoom_window(self):  # Méthode pour ouvrir une fenêtre de zoom
        messagebox.showinfo("Copier", "Sommets copiés dans le presse-papiers.")  # Message de confirmation

        
# Lancer l'application
if __name__ == "__main__":  # Si le script est exécuté directement
    app = Application()  # Crée une instance de l'application
    app.mainloop()  # Démarre la boucle principale de l'application
