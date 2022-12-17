import numpy as np                # Bibliotheque manipulant des entiers de taille arbitraire
import ArbresBinaires             # Classe manipulant la structure de donnee utilisee ici
import math                       # Bibliotheque manipulant les fonctions mathematiques
import os                         # Bibliotheque manipulant les commandes sur le systeme
import matplotlib.pyplot as plt   # Bibliotheque permettant de tracer les graphes de l'experience 
import time                       # Bibliotheque manipulant le temps pour chronométrer les experiences
from tabulate import tabulate     # Bibliotheque manipulant l'affichage sous forme de tableau dans le terminal
from datetime import timedelta    # Bibliotheque manipulant le formattage du temps en hh::mm::ss
# ----------------------------------------------------------------------------------- #
identf = 0    # Variable globale pour identifier les noeuds pour l'affichage sous format dot
# ----------------------------------------------------------------------------------- #
# ---------------------------- PARTIE I --------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# Fonction renvoyant une liste de bits representant la decomposition en base 2 de l’entier x, 
# telle que les bits de poids les plus faibles soient presentes en tete de liste
def decomposition(x):
  LR = []
  if (x == 0): return LR
  binX = bin(x)[2:]       # A partir du 2eme car les 2 premiers caracteres sont '0b' 
  for i in binX:
    if (i == '1'): LR.insert(0, True)
    elif (i == '0'): LR.insert(0, False)

  return LR
# ----------------------------------------------------------------------------------- #
# Fonction renvoyant soit la liste tronquee ne contenant que ses n premiers elements,
# soit la liste completee a droite par des valeurs False, de taille n. 
def completion(Liste, n):
  if (n <= len(Liste)): return Liste[:n]
  else:
    difference = n - len(Liste)
    for i in range(difference):
      Liste.append(False)
  return Liste
# ----------------------------------------------------------------------------------- #
# Fonction qui decompose x en base 2 et qui complete la liste obtenue afin qu’elle soit de taille n.
def table(x, n):
  return completion(decomposition(x), n)
# ----------------------------------------------------------------------------------- #
# ---------------------------- PARTIE II -------------------------------------------- #
# ----------------------------------------------------------------------------------- #
#  Fonction qui construit l’arbre de decision associe a la table de verite 'table'.
def cons_arbre(table):
  global identf                           # Pour acceder a la variable globale
  h = int(math.log(len(table), 2))        # Hauteur de l'arbre
  root = ArbresBinaires.ArbreBinaire("x" + str(h), identf) # Creation de la racine
  res = build(h, table, root, pow(2, h))  # Constrution de la suite de l'arbre avec build

  return res
# ----------------------------------------------------------------------------------- #
# Fonction permettant de construire recursivement l'arbre de decision associe a la table de 
# verite 'table'
def build(h, table, tree, pos_tab):
  # h: hauteur/etage
  # table: table de verite 
  # tree: arbre courant
  # pos_tab: position de la feuille la plus a droite dans 'table'
  global identf   # Pour acceder a la variable globale
  if (h == 1):    # Si l'on est aux feuilles             
    identf += 1
    tree.enfant_gauche = ArbresBinaires.ArbreBinaire(table[int(pos_tab - 2)], identf)
    identf += 1
    tree.enfant_droit = ArbresBinaires.ArbreBinaire(table[int(pos_tab - 1)], identf)
  else:           # Si l'on est pas aux feuilles
    identf += 1
    tree.enfant_gauche = ArbresBinaires.ArbreBinaire("x" + str(h - 1), identf)
    build(h - 1, table, tree.enfant_gauche, pos_tab - pow(2, h - 1))
    identf += 1
    tree.enfant_droit = ArbresBinaires.ArbreBinaire("x" + str(h - 1), identf)
    build(h - 1, table, tree.enfant_droit, pos_tab)
  return tree
# ----------------------------------------------------------------------------------- #
# Fonction permettant d'ecrire un lien entre le pere et le fils s'il n'a pas deja ete ecrit dans un fichier.dot
def dot(pere, fils, orientation, existance):
  # pere: noeud pere dans le  lien
  # fils: noeud fils dans le lien
  # orientation: 1 si fils gauche et -1 si fils droit
  fichier = open("graphe.dot", 'a')
  if (orientation > 0):  # Gauche
    if ("\t" + "\"" + str(pere) + "\"" + " -> " + "\"" + str(fils) + "\"" + "[color=\"green\"];\n") not in existance:
      fichier.write("\t" + "\"" + str(pere) + "\"" + " -> " + "\"" + str(fils) + "\"" + "[color=\"green\"];\n")
      existance["\t" + "\"" + str(pere) + "\"" + " -> " + "\"" + str(fils) + "\"" + "[color=\"green\"];\n"] = "ok"
  else:  # Droite
    if ("\t" + "\"" + str(pere) + "\"" + " -> " + "\"" + str(fils) + "\"" + "[style=\"dotted\", color=\"red\"];\n") not in existance:
      fichier.write("\t" + "\"" + str(pere) + "\"" + " -> " + "\"" + str(fils) + "\"" + "[style=\"dotted\", color=\"red\"];\n")
      existance["\t" + "\"" + str(pere) + "\"" + " -> " + "\"" + str(fils) + "\"" + "[style=\"dotted\", color=\"red\"];\n"] = "ok"
  fichier.close()
# ----------------------------------------------------------------------------------- #
# Fonction qui parcours l'arbre 'tree' et envoie a la fonction dot les liens a ecrire dans un fichier .dot
def parcours_dot(tree, existance):
  if (tree != None):
    if (tree.enfant_gauche != None):
      dot(
        str(tree.valeur) + "_" + str(tree.id),
        str(tree.enfant_gauche.valeur) + "_" + str(tree.enfant_gauche.id), 1,
        existance)
      parcours_dot(tree.enfant_gauche, existance)
    if (tree.enfant_droit != None):
      dot(
        str(tree.valeur) + "_" + str(tree.id),
        str(tree.enfant_droit.valeur) + "_" + str(tree.enfant_droit.id), -1,
        existance)
      parcours_dot(tree.enfant_droit, existance)
  # Cas particulier ou il n'y a qu'un seul noeud dans l'arbre
  if (tree != None) and (tree.enfant_gauche == None) and (tree.enfant_droit == None) and (len(existance) == 0):
    fichier = open("graphe.dot", 'a')
    fichier.write(str(tree.valeur) + "\n")
    fichier.close()
# ----------------------------------------------------------------------------------- #
# Fonction qui a chaque noeud de l'arbre associe le mot de Lukasiewicz
def luka(tree, text):
  if (tree.enfant_gauche != None):
    text_gauche = luka(tree.enfant_gauche, text)
    text = str(tree.valeur) + "(" + text_gauche + ")"
    if (tree.enfant_droit != None):
      text_droit = luka(tree.enfant_droit, text)
      text = text + "(" + text_droit + ")"
      tree.valeur = text
  else:
    text = str(tree.valeur)
  return text
# ----------------------------------------------------------------------------------- #
# Fonction qui compresse l'arbre en fusionnant les sous-arbres isomorphe
def luka_compresse(tree, dict):
  global identf
  if (tree.enfant_gauche != None):
    if not (tree.enfant_gauche.valeur in dict.keys()):
      identf += 1
      dict[tree.enfant_gauche.valeur] = tree.enfant_gauche
      luka_compresse(tree.enfant_gauche, dict)
    else:
      tree.enfant_gauche = dict[tree.enfant_gauche.valeur]

  if (tree.enfant_droit != None):
    if not (tree.enfant_droit.valeur in dict.keys()):
      identf += 1
      dict[tree.enfant_droit.valeur] = tree.enfant_droit
      luka_compresse(tree.enfant_droit, dict)
    else:
      tree.enfant_droit = dict[tree.enfant_droit.valeur]
# ----------------------------------------------------------------------------------- #
# ---------------------------- PARTIE III ------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# Fonction qui compresse le DAG en appliquant la Deletion Rule
def compression_bdd2(tree):
  if (tree != None):
    if (tree.enfant_gauche != None) and (tree.enfant_droit != None):
      if (tree.enfant_gauche.valeur == tree.enfant_droit.valeur):
        tree.remplace_tree(tree.enfant_gauche)
        compression_bdd2(tree)
      else:
        compression_bdd2(tree.enfant_gauche)
        compression_bdd2(tree.enfant_droit)
# ----------------------------------------------------------------------------------- #
# ---------------------------- PARTIE IV -------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# Fonction qui permet de compter le nombre de noeuds differents dans un arbre
def parcours_nb_noeuds(tree, tab):
  if (tree == None): return 0
  else:
    res = 1
    tab.append(tree.valeur)
    if (tree.enfant_gauche != None):
      if not (tree.enfant_gauche.valeur in tab):
        res += parcours_nb_noeuds(tree.enfant_gauche, tab)
    if (tree.enfant_droit != None):
      if not (tree.enfant_droit.valeur in tab):
        res += parcours_nb_noeuds(tree.enfant_droit, tab)
    return res
# ----------------------------------------------------------------------------------- #
# Fonction qui permet de retourner le dictionnaire contenant les noeuds et le nombre de fonctions 
# booleenes pour toutes les combinaisons d'ROBDDs d'une variable donnee 'nbVariables'
def create_coubres(nbVariables, affichage):
  global identf
  dicRes = {}
  valMax = 2**(2**nbVariables) 
  nbSamples = 0 # Nombre d'echantillons 
  mult = 1
  # Samples de l'article
  if (nbVariables == 5): mult = valMax//500_003
  if (nbVariables == 6): mult = valMax//400_003
  if (nbVariables == 7): mult = valMax//486_892
  if (nbVariables == 8): mult = valMax//56_343
  if (nbVariables == 9): mult = valMax//94_999
  if (nbVariables == 10): mult = valMax//17_975

  if (affichage):
    if not os.path.exists("Graphes" + str(nbVariables) + "/"):
      os.mkdir("Graphes" + str(nbVariables))

  for i in range(valMax):
    i = i*mult
    if (i > 2**(2**nbVariables)): break
    nbSamples += 1 
    identf = 0
    tree = cons_arbre(table(i, int(math.log2(valMax))))
    luka(tree, "")
    luka_compresse(tree, {})
    compression_bdd2(tree)

    if (affichage):
      os.remove("graphe.dot")
      fichier = open("graphe.dot", 'a')
      fichier.write("digraph {\n")
      fichier.close()
      existance = {}
      parcours_dot(tree, existance)
      fichier = open("graphe.dot", 'a')
      fichier.write("}")
      fichier.close()
      os.system("dot -Tpng graphe.dot -o ./Graphes" + str(nbVariables) +"/graphe" + str(i) + ".png")

    tab = []
    nbNoeuds = parcours_nb_noeuds(tree, tab)
    if nbNoeuds not in dicRes.keys():
      dicRes[nbNoeuds] = 1
    else:
      dicRes[nbNoeuds] += 1
  
  return (dicRes, nbSamples)
# ----------------------------------------------------------------------------------- #
# Fonction qui permet d'afficher le format des secondes en hh::mm::ss
def temps_vers_format(tempsSec):
    td_str = str(timedelta(seconds=round(tempsSec)))

    x = td_str.split(':')
    return x[0]+":"+x[1]+":"+x[2]
# ----------------------------------------------------------------------------------- #
# ---------------------------- PARTIE V --------------------------------------------- #
# ----------------------------------------------------------------------------------- #
# Fonction qui permet de recuperer e.g: '55' dans le mot de Luka: 'x55(x44(True)x33(....)) 
def recup_numero_luka(motLuka):
  taille = len(motLuka)
  if (taille <= 1): return -1
  i = 1
  recup = ""
  while ((i < taille) and (motLuka[i] != "(")):
    recup += motLuka[i]
    i += 1 
  
  return int(recup)
# ----------------------------------------------------------------------------------- #
# Fonction qui permet de faire la fusion entre 2 ROBDD 'tree1' et 'tree2' dans 'treeRes'
def fusion_ROBDD(tree1, tree2, treeRes):
  global identf
  # Cas basiques
  if (tree1 == None): 
    if (tree2 == None): return None
    else: return tree2
  elif (tree2 == None): return tree1

  text = ""
  valeur1 = -1
  valeur2 = -1
  if (str(tree1.valeur)[0] == "T"):
    valeur1 = -1  # -1 pour True
  elif (str(tree1.valeur)[0] == "F"):
    valeur1 = -2  # -2 pour False
  else:
    valeur1 = recup_numero_luka(tree1.valeur)

  if (str(tree2.valeur)[0] == "T"): 
    valeur2 = -1  # -1 pour True
  elif (str(tree2.valeur)[0] == "F"):
    valeur2 = -2  # -2 pour False
  else:
    valeur2 = recup_numero_luka(tree2.valeur)

  if ((valeur1 < 0) and (valeur2 < 0)):
    valeur1Bis = True 
    valeur2BIs = True 
    if (valeur1 == -1): valeur1Bis = True
    if (valeur1 == -2): valeur1Bis = False
    if (valeur2 == -1): valeur2Bis = True
    if (valeur2 == -2): valeur2Bis = False 
    res = valeur1Bis ^ valeur2Bis # XOR
    return str(res)

  treeRes.enfant_gauche = ArbresBinaires.ArbreBinaire("", identf); identf += 1
  treeRes.enfant_droit = ArbresBinaires.ArbreBinaire("", identf); identf += 1
    
  if ((valeur1 < 0) and (valeur2 > 0)):
    treeRes.enfant_gauche = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1, tree2.enfant_gauche, treeRes.enfant_gauche), identf); identf += 1
    treeRes.enfant_droit = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1, tree2.enfant_droit, treeRes.enfant_droit), identf); identf += 1
    text += "x" + str(valeur2)
    text += "(" + treeRes.enfant_gauche.valeur + ")"
    text += "(" + treeRes.enfant_droit.valeur + ")"
    treeRes.valeur = text 
    return treeRes.valeur

  if ((valeur1 > 0) and (valeur2 < 0)):
    treeRes.enfant_gauche = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1.enfant_gauche, tree2, treeRes.enfant_gauche), identf); identf += 1
    treeRes.enfant_droit = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1.enfant_droit, tree2, treeRes.enfant_droit), identf); identf += 1
    text += "x" + str(valeur1)
    text += "(" + treeRes.enfant_gauche.valeur + ")"
    text += "(" + treeRes.enfant_droit.valeur + ")"
    treeRes.valeur = text 
    return treeRes.valeur

  if ((valeur1 > 0) and (valeur2 > 0)):
    if (valeur1 == valeur2):
      treeRes.enfant_gauche = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1.enfant_gauche, tree2.enfant_gauche, treeRes.enfant_gauche), identf); identf += 1
      treeRes.enfant_droit = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1.enfant_droit, tree2.enfant_droit, treeRes.enfant_droit), identf); identf += 1
      text += "x" + str(valeur1) 
      text += "(" + treeRes.enfant_gauche.valeur + ")"
      text += "(" + treeRes.enfant_droit.valeur + ")"
      treeRes.valeur = text
      return treeRes.valeur

    elif (valeur1 > valeur2):
      treeRes.enfant_gauche = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1, tree2.enfant_gauche, treeRes.enfant_gauche), identf); identf += 1
      treeRes.enfant_droit = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1, tree2.enfant_droit, treeRes.enfant_droit), identf); identf += 1
      text += "x" + str(valeur2) 
      text += "(" + treeRes.enfant_gauche.valeur + ")"
      text += "(" + treeRes.enfant_droit.valeur + ")"
      treeRes.valeur = text
      return treeRes.valeur
    else: # (valeur1 < valeur2)
      treeRes.enfant_gauche = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1.enfant_gauche, tree2, treeRes.enfant_gauche), identf); identf += 1
      treeRes.enfant_droit = ArbresBinaires.ArbreBinaire(fusion_ROBDD(tree1.enfant_droit, tree2, treeRes.enfant_droit), identf); identf += 1
      text += "x" + str(valeur1) 
      text += "(" + treeRes.enfant_gauche.valeur + ")"
      text += "(" + treeRes.enfant_droit.valeur + ")"
      treeRes.valeur = text
      return treeRes.valeur
# ----------------------------------------------------------------------------------- #
# Fonction qui permet de mettre a jour les etiquettes des ROBDDs
def luka_after(tree, text):
  # etageActuel = int(tree.valeur[1])
  if (tree.enfant_gauche != None):
    text_gauche = luka_after(tree.enfant_gauche, text)
    text = "x" + str(recup_numero_luka(tree.valeur)) + "(" + text_gauche + ")"
    if (tree.enfant_droit != None):
      text_droit = luka_after(tree.enfant_droit, text)
      text = text + "(" + text_droit + ")"
      tree.valeur = text
  else:
    text = str(tree.valeur)
  return text
# ----------------------------------------------------------------------------------- #
# ------------------------------------TESTS------------------------------------------ #
# ----------------------------------------------------------------------------------- #
print("===================== Partie I =====================")
nombre = np.random.randint(0, 100) # A CHANGER POUR LES TESTS 
print("Nombre: " + str(nombre))
print("Decomposition en binaire: "+bin(nombre))
RES = decomposition(nombre)
print("Decomposition avec la fonction: "+str(RES))
n = 5  # A CHANGER POUR LES TESTS 
print("Completion avec la fonction et avec n="+str(n)+": "+str(completion(RES, n)))
print("Table de verité de "+str(nombre)+" de taille "+str(n)+": "+ str(table(nombre, n)))
print("===================== Partie II =====================")
# Manipulation pour l'ecriture dans un .dot
os.remove("graphe.dot") 
fichier = open("graphe.dot", 'a')
fichier.write("digraph {\n")
fichier.close()
nombre = 38   # A CHANGER POUR LES TESTS 
taille = 8    # A CHANGER POUR LES TESTS 
tree = cons_arbre(table(nombre, taille))
# tree = cons_arbre(table(int('01100011', 2) ,8))
# Manipulation pour l'ecriture dans un .dot
existance = {}   # Sert pour voir si l'on a pas deja parcourut un noeud
parcours_dot(tree, existance) 
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tpng graphe.dot -o ./Graphes/graphe.png")
print("Voir ./Graphes/graphe.png pour l'affichage de l'arbre de decision table("+str(nombre)+", "+str(n)+")")

# Manipulation pour l'ecriture dans un .dot
os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("digraph {\n")
fichier.close()
luka(tree, "")
# Manipulation pour l'ecriture dans un .dot
existance = {}  # Sert pour voir si l'on a pas deja parcourut un noeud
parcours_dot(tree, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tpng graphe.dot -o ./Graphes/graphe2.png")
print("Voir ./Graphes/graphe2.png pour l'affichage de l'arbre de decision table("+str(nombre)+", "+str(n)+") avec les mots de Luka")

# Manipulation pour l'ecriture dans un .dot
os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("digraph {\n")
fichier.close()
dict = {}  
identf = 0     # Pour remettre a 0 la variable globale
luka_compresse(tree, dict)
existance = {}
parcours_dot(tree, existance)
# Manipulation pour l'ecriture dans un .dot
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tpng graphe.dot -o ./Graphes/graphe3.png")
print("Voir ./Graphes/graphe3.png pour l'affichage de l'arbre de decision table("+str(nombre)+", "+str(n)+") compresse avec les mots de Luka")
print("===================== Partie III =====================")
# Manipulation pour l'ecriture dans un .dot
os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("digraph {\n")
fichier.close()
compression_bdd2(tree)
existance = {}
parcours_dot(tree, existance)
# Manipulation pour l'ecriture dans un .dot
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tpng graphe.dot -o ./Graphes/graphe4.png")
print("Voir ./Graphes/graphe4.png pour l'affichage de l'arbre de decision table("+str(nombre)+", "+str(n)+") transforme en ROBDD")
print("===================== Partie IV =====================")
tableau = [['No. Variables(n)', 'No. Samples', 'No. Unique Sizes', 'Compute Time hh::mm::ss', 'Seconds per ROBDD']]
nombreVariables = 5   # A CHANGER POUR LES TESTS 
for i in range (1, nombreVariables):  # de 1 a nombreVariables-1 ATTENTION
  t0 = time.time()
  dictRes, nbSamples = create_coubres(i, False)  # A CHANGER PAR True SI ON SOUHAITE AFFICHER TOUS LES GRPAHES (ATTENTION LONG POUR nombreVariables GRAND)
  t1 = time.time() - t0
  tableau.insert(i, [str(i), str(nbSamples), len(dictRes), temps_vers_format(t1), str(t1/nbSamples)])
  print("Nombre variables "+str(i)+": "+str(dictRes))
  listeDict = dictRes.items()
  listeDict = sorted(listeDict)
  x, y = zip(*listeDict)
  plt.title("ROBDD node count for "+str(i)+" variable")
  plt.xlabel("No. nodes")
  plt.ylabel("Number of Boolean functions")
  plt.plot(x, y, "o-", color ="green")
  plt.grid(visible=True)
  if not os.path.exists("Figures"):
    os.mkdir("Figures")
  plt.savefig("Figures/ROBDD_node_count_for_"+str(i)+"_variable.png")
  # plt.show()  # Decommenter si on veut l'afficher avec le terminal
  
os.remove("data.txt")
fichier = open("data.txt", 'a')
fichier.write(tabulate(tableau, headers='firstrow', tablefmt='fancy_grid'))
fichier.close()

print(tabulate(tableau, headers='firstrow', tablefmt='fancy_grid'))
print("Voir ./Figures/ pour les courbes traces pour les variables allant de 1 a "+str(nombreVariables))
print("===================== Partie V =====================")
identf = 0
tree1 = cons_arbre(table(int('0111', 2), 4))    # TABLE A CHANGER POUR D'AUTRES TESTS
luka(tree1, "")
luka_compresse(tree1, {})
compression_bdd2(tree1)
luka_after(tree1, "")
# Manipulation pour l'ecriture dans un .dot
os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("digraph {\n")
fichier.close()
existance = {}
parcours_dot(tree1, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tpng graphe.dot -o ./Graphes/ROBDD_a_fusionner_1.png")

identf = 0
tree2 = cons_arbre(table(int('1000', 2), 4))  # TABLE A CHANGER POUR D'AUTRES TESTS
luka(tree2, "")
luka_compresse(tree2, {})
compression_bdd2(tree2)
luka_after(tree2, "")
# Manipulation pour l'ecriture dans un .dot
os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("digraph {\n")
fichier.close()
existance = {}
parcours_dot(tree2, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tpng graphe.dot -o ./Graphes/ROBDD_a_fusionner_2.png")

identf = 0
tree3 = ArbresBinaires.ArbreBinaire("", 0)
fusion_ROBDD(tree1, tree2, tree3)
luka_compresse(tree3, {})
compression_bdd2(tree3)
# Manipulation pour l'ecriture dans un .dot
os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("digraph {\n")
fichier.close()
existance = {}
parcours_dot(tree3, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tpng graphe.dot -o ./Graphes/ROBDD_fusionne.png")
print("Voir les deux ROBDD a fusionner dans ./Graphes/ROBDD_a_fusionner_1.png et ./Graphes/ROBDD_a_fusionner_2.png\net l'ROBDD fusionne dans ./Graphes/ROBDD_fusionne.png")
print("===================== Autres tests =====================")
nbVar = 10            # A CHANGER POUR D'AUTRES TESTS
nbTable = (2**100)+1  # A CHANGER POUR D'AUTRES TESTS
valMax = 2**(2**nbVar) 
tree = cons_arbre(table(nbTable, int(math.log2(valMax))))
luka(tree, "")
luka_compresse(tree, {})
tab = []
dicRes = {}
nbNoeuds = parcours_nb_noeuds(tree, tab)
if nbNoeuds not in dicRes.keys():
  dicRes[nbNoeuds] = 1
else:
  dicRes[nbNoeuds] += 1
print("Compression => Table de verite nb: "+str(nbTable)+" | "+str(nbVar)+" variables: "+str(dicRes))
compression_bdd2(tree)
tab = []
dicRes = {}
nbNoeuds = parcours_nb_noeuds(tree, tab)
if nbNoeuds not in dicRes.keys():
  dicRes[nbNoeuds] = 1
else:
  dicRes[nbNoeuds] += 1
print("Compression_bdd => Table de verite nb: "+str(nbTable)+" | "+str(nbVar)+" variables: "+str(dicRes))


