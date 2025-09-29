from colorama import init, Fore, Style
init(autoreset=True)

# Classe Dungeon pour représenter la grille et placer les éléments
import random

class Dungeon:
    def __init__(self, taille=5):
        self.taille = taille
        self.grille = [[None for _ in range(taille)] for _ in range(taille)]
        self.monstres = [] # pas utilisé pour le moment
        self.epees = [] # pas utilisé pour le moment
        self.sortie = None # pas utilisé pour le moment
        self._placer_elements()

    def _placer_elements(self):
        # Exclure la position (0,0) du pool de positions
        positions = [(x, y) for x in range(self.taille) for y in range(self.taille) if not (x == 0 and y == 0)]
        random.shuffle(positions)
        
        # Placer 10 monstres
        for _ in range(10):
            x, y = positions.pop()
            self.grille[x][y] = 'M'
            self.monstres.append((x, y))
        
        # Placer 5 épées
        for _ in range(5):
            x, y = positions.pop()
            self.grille[x][y] = 'E'
            self.epees.append((x, y))
        
        # Placer la sortie
        x, y = positions.pop()
        self.grille[x][y] = 'S'
        self.sortie = (x, y)

    def afficher(self, aventurier=None):
        print("  ", end="")
        for x in range(self.taille):
            print(f" {x} ", end="")
        print()
        for y in range(self.taille):
            print(f"{y} ", end="")
            for x in range(self.taille):
                if aventurier and x == aventurier.position_x and y == aventurier.position_y:
                    print(Fore.BLUE + " H " + Style.RESET_ALL, end="")
                else:
                    case = self.grille[x][y]
                    if case is None:
                        print(" . ", end="")
                    elif case == 'M':
                        print(Fore.RED + " M " + Style.RESET_ALL, end="")
                    elif case == 'E':
                        print(Fore.YELLOW + " E " + Style.RESET_ALL, end="")
                    elif case == 'S':
                        print(Fore.GREEN + " S " + Style.RESET_ALL, end="")
                    else:
                        print(f" {case} ", end="")
            print()

# Classe Aventurier pour représenter un héros
class Aventurier:
    def __init__(self, nom):
        self.nom = nom
        self.agilite = 10
        self.sante = 5
        self.position_x = 0
        self.position_y = 0
        self.monstres_vaincus = 0

    def __repr__(self):
        return (f"Aventurier(nom={self.nom}, agilité={self.agilite}, "
                f"santé={self.sante}, position=({self.position_x},{self.position_y}))")
    
    def attaquer(self):
        import random
        valeur = random.randint(0, self.agilite)
        print(f"Vous attaquez un monstre ! Jet : {valeur} (objectif : 5 ou plus)")
        return valeur >= 5
    
    def deplacer(self, dx, dy, taille_donjon, donjon=None):
        """Déplace l'aventurier de dx sur l'axe x et de dy sur l'axe y, si possible. Gère les épées."""
        new_x = self.position_x + dx
        new_y = self.position_y + dy

        #si on ne sort pas du donjon
        if 0 <= new_x < taille_donjon and 0 <= new_y < taille_donjon:
            self.position_x = new_x
            self.position_y = new_y

            # Gestion de l'épée
            if donjon and donjon.grille[new_x][new_y] == 'E':
                donjon.grille[new_x][new_y] = None
                self.agilite += 2
                print(Fore.YELLOW + "Vous avez trouvé une arme, vous gagnez 2 points d'agilité !" + Style.RESET_ALL)
            
            # Gestion du monstre
            elif donjon and donjon.grille[new_x][new_y] == 'M':
                while donjon.grille[new_x][new_y] == 'M' and self.sante > 0:
                    
                    if self.attaquer():
                        donjon.grille[new_x][new_y] = None
                        self.monstres_vaincus += 1
                        print(Fore.GREEN + "Vous avez vaincu un monstre." + Style.RESET_ALL)
                        break
                    
                    else:
                        self.sante -= 1
                        print(Fore.RED + f"Vous êtes blessé. Santé restante : {self.sante}" + Style.RESET_ALL)
                        
                        if self.sante <= 0:
                            print("Vous êtes mort.")
                            import sys
                            sys.exit()
                        
                        # Proposer de continuer ou fuir
                        reponse = input("Voulez-vous attaquer à nouveau ? (o/n) : ").strip().lower()
                        if reponse != 'o':
                            print("Vous fuyez le combat !")
                            break
            
            # Gestion de la sortie
            elif donjon and donjon.grille[new_x][new_y] == 'S':
                print(Fore.GREEN + f"Bravo vous vous êtes échappé du donjon ! Monstres vaincus : {self.monstres_vaincus}" + Style.RESET_ALL)
                import sys
                sys.exit()
            
            print(f"Nouvelle position : ({self.position_x}, {self.position_y})")
        
        else:
            print("Déplacement incorrect : hors du donjon !")
        
        print(f"Santé : {self.sante} | Agilité : {self.agilite}")


# Exemple d'utilisation

# Version Windows uniquement
def get_arrow_key():
    import msvcrt
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':
            key2 = msvcrt.getch()
            if key2 == b'H':
                return 'UP'
            elif key2 == b'P':
                return 'DOWN'
            elif key2 == b'K':
                return 'LEFT'
            elif key2 == b'M':
                return 'RIGHT'
        elif key == b'q':
            return 'QUIT'

if __name__ == "__main__":
    hero = Aventurier("Arthur")
    print(repr(hero))
    
    print("\nDonjon généré :")
    donjon = Dungeon()
    donjon.afficher(aventurier=hero)
    
    print("\nUtilisez les flèches pour déplacer le héros (H).\nAppuyez sur 'q' pour quitter.")
    while True:
        key = get_arrow_key()
        if key == 'QUIT':
            print("Fin du jeu.")
            break
        elif key == 'UP':
            hero.deplacer(0, -1, donjon.taille, donjon)
        elif key == 'DOWN':
            hero.deplacer(0, 1, donjon.taille, donjon)
        elif key == 'LEFT':
            hero.deplacer(-1, 0, donjon.taille, donjon)
        elif key == 'RIGHT':
            hero.deplacer(1, 0, donjon.taille, donjon)
        
        donjon.afficher(aventurier=hero)


	

