import numpy as np
import ArbresBinaires
import math
import os
import copy
import matplotlib.pyplot as plt
import time
from tabulate import tabulate
from datetime import timedelta

identf = 0


# ----------------------------------------------------------------------------------- #
def decomposition(x):
  LR = []
  if (x == 0): return LR
  binX = bin(x)[2:]
  for i in binX:
    if (i == '1'): LR.insert(0, True)
    elif (i == '0'): LR.insert(0, False)

  return LR


# ----------------------------------------------------------------------------------- #
def completion(Liste, n):
  if (n <= len(Liste)): return Liste[:n]
  else:
    difference = n - len(Liste)
    for i in range(difference):
      Liste.append(False)
  return Liste


# ----------------------------------------------------------------------------------- #
def table(x, n):
  return completion(decomposition(x), n)


# ----------------------------------------------------------------------------------- #
#Question 2.9
def cons_arbre(table):
  global identf
  # os.remove("graphe.dot")
  # fichier = open("graphe.dot", 'a')
  # fichier.write("graph {\n")
  # fichier.close()

  h = int(math.log(len(table), 2))
  root = ArbresBinaires.ArbreBinaire("x" + str(h), identf)
  res = build(h, table, root, pow(2, h))

  # fichier = open("graphe.dot", 'a')
  # fichier.write("}")
  # fichier.close() 

  return res


# ----------------------------------------------------------------------------------- #
def build(h, table, tree, pos_tab):
  global identf
  #pos_tab: indique les contenue de feuilles se situe à quelle position dans le tableau
  #h:etage
  tree.valeur = "x" + str(h)
  if (h == 1):
    # print(str(pos_tab) + " etage: " + str(h))
    identf += 1
    tree.enfant_gauche = ArbresBinaires.ArbreBinaire(table[int(pos_tab - 2)],
                                                     identf)
    # dot(tree.valeur + "_" + str(int(pos_tab)),
    #     str(tree.enfant_gauche.valeur) + "_" + str(int(pos_tab - 2)))
    identf += 1
    tree.enfant_droit = ArbresBinaires.ArbreBinaire(table[int(pos_tab - 1)],
                                                    identf)
    # dot(tree.valeur + "_" + str(int(pos_tab)),
    #     str(tree.enfant_droit.valeur) + "_" + str(int(pos_tab - 1)))
  else:
    # print(str(pos_tab) + " etage: " + str(h))
    identf += 1
    tree.enfant_gauche = ArbresBinaires.ArbreBinaire("x" + str(h - 1), identf)
    # dot(tree.valeur + "_" + str(int(pos_tab)),
    #     tree.enfant_gauche.valeur + "_" + str(pos_tab - pow(2, h - 1)))
    build(h - 1, table, tree.enfant_gauche, pos_tab - pow(2, h - 1))
    identf += 1
    tree.enfant_droit = ArbresBinaires.ArbreBinaire("x" + str(h - 1), identf)
    # dot(tree.valeur + "_" + str(int(pos_tab)),
    #     tree.enfant_droit.valeur + "_" + str(pos_tab))
    build(h - 1, table, tree.enfant_droit, pos_tab)
  return tree


# ----------------------------------------------------------------------------------- #
def dot(pere, fils, orientation, existance):
  fichier = open("graphe.dot", 'a')
  if (orientation > 0):  # Gauche
    if ("\t" + "\"" + str(pere) + "\"" + " -- " + "\"" + str(fils) + "\"" +
        "[style=\"dotted\"];\n") not in existance:
      fichier.write("\t" + "\"" + str(pere) + "\"" + " -- " + "\"" +
                    str(fils) + "\"" + "[style=\"dotted\"];\n")
      existance["\t" + "\"" + str(pere) + "\"" + " -- " + "\"" + str(fils) +
                "\"" + "[style=\"dotted\"];\n"] = "ok"
  else:  # Droite
    if ("\t" + "\"" + str(pere) + "\"" + " -- " + "\"" + str(fils) + "\"" +
        ";\n") not in existance:
      fichier.write("\t" + "\"" + str(pere) + "\"" + " -- " + "\"" +
                    str(fils) + "\"" + ";\n")
      existance["\t" + "\"" + str(pere) + "\"" + " -- " + "\"" + str(fils) +
                "\"" + ";\n"] = "ok"
  fichier.close()


# ----------------------------------------------------------------------------------- #
def luka(tree, text):
  # etageActuel = int(tree.valeur[1])
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
def luka_after(tree, text):
  # etageActuel = int(tree.valeur[1])
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
  if (tree != None) and (tree.enfant_gauche
                         == None) and (tree.enfant_droit
                                       == None) and (len(existance) == 0):
    fichier = open("graphe.dot", 'a')
    fichier.write(str(tree.valeur) + "\n")
    fichier.close()


# ----------------------------------------------------------------------------------- #
def luka_compresse(tree, dict):
  global identf
  if (tree.enfant_gauche != None):
    if not (tree.enfant_gauche.valeur in dict.keys()):
      identf += 1
      dict[tree.enfant_gauche.valeur] = tree.enfant_gauche
      # identf += 1
      # tree.enfant_gauche.id = identf
      # dot(tree.valeur + "_" + str(tree.id),
      #     tree.enfant_gauche.valeur + "_" + str(tree.enfant_gauche.id))
      luka_compresse(tree.enfant_gauche, dict)
    else:
      # tree.enfant_gauche = None
      # tree.enfant_gauche.enfant_gauche = None
      # tree.enfant_gauche.enfant_droit = None
      # print("===="+ str(dict[tree.enfant_gauche.valeur].valeur))
      tree.enfant_gauche = dict[tree.enfant_gauche.valeur]
      # luka_compresse(tree.enfant_droit, dict)
      # luka_compresse(tree.enfant_gauche, dict)
      # tree.enfant_gauche.enfant_gauche = None
      # dot(tree.valeur + "_" + str(tree.id),
      #     tree.enfant_gauche.valeur + "_" + str(tree.enfant_gauche.id))

  if (tree.enfant_droit != None):
    if not (tree.enfant_droit.valeur in dict.keys()):
      identf += 1
      dict[tree.enfant_droit.valeur] = tree.enfant_droit
      # identf += 1
      # tree.enfant_droit.id = identf
      # dot(tree.valeur + "_" + str(tree.id),
      #     tree.enfant_droit.valeur + "_" + str(tree.enfant_droit.id))
      luka_compresse(tree.enfant_droit, dict)
    else:
      # print("===="+ str(dict[tree.enfant_droit.valeur].valeur))
      tree.enfant_droit = dict[tree.enfant_droit.valeur]
      # luka_compresse(tree.enfant_droit, dict)
      # luka_compresse(tree.enfant_gauche, dict)
      # tree.enfant_gauche.enfant_gauche = None
      # tree.enfant_gauche.enfant_droit = None
      # tree.enfant_droit = None

      # dot(tree.valeur + "_" + str(tree.id),
      #     tree.enfant_droit.valeur + "_" + str(tree.enfant_droit.id))


# ----------------------------------------------------------------------------------- #
def compression_bdd(tree):
  if (tree.enfant_gauche != None):
    if (tree.enfant_gauche.enfant_gauche !=
        None) and (tree.enfant_gauche.enfant_droit != None):
      if (tree.enfant_gauche.enfant_gauche.valeur ==
          tree.enfant_gauche.enfant_droit.valeur):
        tree.enfant_gauche = tree.enfant_gauche.enfant_gauche
      compression_bdd(tree.enfant_gauche)
  if (tree.enfant_droit != None):
    if (tree.enfant_droit.enfant_gauche !=
        None) and (tree.enfant_droit.enfant_droit != None):
      if (tree.enfant_droit.enfant_gauche.valeur ==
          tree.enfant_droit.enfant_droit.valeur):
        tree.enfant_droit = tree.enfant_droit.enfant_droit
      compression_bdd(tree.enfant_droit)


# ----------------------------------------------------------------------------------- #
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
def parcours_nb_noeuds2(tree): # Voir pq probleme 
  if (tree == None): return 0
  else:
    res = 1
    tree.visite = True # On la visite 
    if (tree.enfant_gauche != None):
      if (tree.enfant_gauche.visite == False): # Si l'on a pas encore visite ce noeud 
        res += parcours_nb_noeuds2(tree.enfant_gauche)
    if (tree.enfant_droit != None):
      if (tree.enfant_droit.visite == False):  # Si l'on a pas encore visite ce noeud 
        res += parcours_nb_noeuds2(tree.enfant_droit)
    return res 
# ----------------------------------------------------------------------------------- #
def create_coubres(nbVariables):
  global identf
  dicRes = {}
  valMax = 2**(2**nbVariables) 
  valComp = 1_000_000_000

  # if (nbVariables == 5): valMax = 500_000
  # if not os.path.exists("Graphes" + str(nbVariables) + "/"):
  #   os.mkdir("Graphes" + str(nbVariables))
  for i in range(valMax):
    if(nbVariables >= 5): 
      i = 1000*i
    if (i>valMax): break
    if (i>valComp): 
      print("======>"+str(i))
      valComp+=1_000_000_000
    
    # if (i > 1000000): break
    # if(nbVariables == 5): i+=8500
    # if (i == 500_000): break
    identf = 0
    tree = cons_arbre(table(i, int(math.log2(valMax))))
    luka(tree, "")
    luka_compresse(tree, {})
    compression_bdd2(tree)
    # os.remove("graphe.dot")
    # fichier = open("graphe.dot", 'a')
    # fichier.write("graph {\n")
    # fichier.close()
    # existance = {}
    # parcours_dot(tree, existance)
    # fichier = open("graphe.dot", 'a')
    # fichier.write("}")
    # fichier.close()
    # os.system("dot -Tsvg graphe.dot -o ./Graphes" + str(nbVariables) +
    #           "/graphe" + str(i) + ".svg")
    tab = []
    nbNoeuds = parcours_nb_noeuds(tree, tab)
    if nbNoeuds not in dicRes.keys():
      dicRes[nbNoeuds] = 1
    else:
      dicRes[nbNoeuds] += 1
  
  return dicRes
# ----------------------------------------------------------------------------------- #
def temps_vers_format(tempsSec):
    # create timedelta and convert it into string
    td_str = str(timedelta(seconds=round(tempsSec)))

    # split string into individual component
    x = td_str.split(':')
    return x[0]+":"+x[1]+":"+x[2]
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
def luka_after(tree, text):
  # etageActuel = int(tree.valeur[1])
  if (tree.enfant_gauche != None):
    text_gauche = luka(tree.enfant_gauche, text)
    text = "x" + str(recup_numero_luka(tree.valeur)) + "(" + text_gauche + ")"
    if (tree.enfant_droit != None):
      text_droit = luka(tree.enfant_droit, text)
      text = text + "(" + text_droit + ")"
      tree.valeur = text
  else:
    text = "x" + str(recup_numero_luka(tree.valeur))
  return text
# ----------------------------------------------------------------------------------- #
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
  print(str(tree1.valeur)+" | "+str(tree2.valeur))
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
# ----------------------------------------------------------------------------------- #
nombre = np.random.randint(0, 100)
print("Nombre: " + str(nombre))
print(bin(nombre)[2:])
RES = decomposition(nombre)
print(RES)
print(decomposition(0))
print(completion(RES, 8))
print(table(nombre, 8))
os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("graph {\n")
fichier.close()
tree = cons_arbre(table(38, 8))
existance = {}
parcours_dot(tree, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tsvg graphe.dot -o ./Graphes/graphe.svg")

os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("graph {\n")
fichier.close()
print(luka(tree, ""))
print("_____________")
existance = {}
parcours_dot(tree, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tsvg graphe.dot -o ./Graphes/graphe2.svg")

os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("graph {\n")
fichier.close()
dict = {}
identf = 0
luka_compresse(tree, dict)
existance = {}
parcours_dot(tree, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tsvg graphe.dot -o ./Graphes/graphe3.svg")

os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("graph {\n")
fichier.close()
compression_bdd(tree)
existance = {}
tree2 = copy.deepcopy(tree)
parcours_dot(tree, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tsvg graphe.dot -o ./Graphes/graphe4.svg")

os.remove("graphe.dot")
fichier = open("graphe.dot", 'a')
fichier.write("graph {\n")
fichier.close()
compression_bdd2(tree2)
existance = {}
parcours_dot(tree2, existance)
fichier = open("graphe.dot", 'a')
fichier.write("}")
fichier.close()
os.system("dot -Tsvg graphe.dot -o ./Graphes/graphe5.svg")


tableau = [['No. Variables(n)', 'No. Samples', 'No. Unique Sizes', 'Compute Time hh::mm::ss', 'Seconds per ROBDD']]
nombreVariables = 6
for i in range (1, nombreVariables):
  t0 = time.time()
  dictRes = create_coubres(i)
  t1 = time.time() - t0
  # fichier = open("data.txt", 'a')
  # fichier.write(str(i)+"\t\t\t"+str(t1)+"\n")
  # fichier.close()
  tableau.insert(i, [str(i), "X", "X", temps_vers_format(t1), "X"])
  print("\n"+str(i)+" variables: ")
  print(dictRes)
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
  plt.show()
  
os.remove("data.txt")
fichier = open("data.txt", 'a')
fichier.write(tabulate(tableau, headers='firstrow', tablefmt='fancy_grid'))
fichier.close()

print(tabulate(tableau, headers='firstrow', tablefmt='fancy_grid'))
print("----------------------------------")
# valMax = 2**(2**10) 
# tree = cons_arbre(table((2**100)+1, int(math.log2(valMax))))
# luka(tree, "")
# luka_compresse(tree, {})
# compression_bdd2(tree)
# # os.remove("graphe.dot")
# # fichier = open("graphe.dot", 'a')
# # fichier.write("graph {\n")
# # fichier.close()
# # existance = {}
# # parcours_dot(tree, existance)
# # fichier = open("graphe.dot", 'a')
# # fichier.write("}")
# # fichier.close()
# # os.system("dot -Tsvg graphe.dot -o ./Test.svg")
# tab = []
# dicRes = {}
# nbNoeuds = parcours_nb_noeuds(tree, tab)
# if nbNoeuds not in dicRes.keys():
#   dicRes[nbNoeuds] = 1
# else:
#   dicRes[nbNoeuds] += 1
# print(dicRes)

# identf = 0
# tree1 = cons_arbre(table(int('0111', 2), 4))
# luka(tree1, "")
# # luka_compresse(tree1, {})
# # compression_bdd2(tree1)
# # luka_after(tree1, "")
# os.remove("graphe.dot")
# fichier = open("graphe.dot", 'a')
# fichier.write("graph {\n")
# fichier.close()
# existance = {}
# parcours_dot(tree1, existance)
# fichier = open("graphe.dot", 'a')
# fichier.write("}")
# fichier.close()
# os.system("dot -Tsvg graphe.dot -o ./Test8.svg")

# identf = 0
# tree2 = cons_arbre(table(int('1000', 2), 4))
# luka(tree2, "")
# luka_compresse(tree2, {})
# compression_bdd2(tree2)
# os.remove("graphe.dot")
# fichier = open("graphe.dot", 'a')
# fichier.write("graph {\n")
# fichier.close()
# existance = {}
# parcours_dot(tree2, existance)
# fichier = open("graphe.dot", 'a')
# fichier.write("}")
# fichier.close()
# os.system("dot -Tsvg graphe.dot -o ./Test1.svg")

# identf = 0
# tree3 = ArbresBinaires.ArbreBinaire("", 0)
# fusion_ROBDD(tree1, tree2, tree3)
# luka_compresse(tree3, {})
# # compression_bdd2(tree3)
# os.remove("graphe.dot")
# fichier = open("graphe.dot", 'a')
# fichier.write("graph {\n")
# fichier.close()
# existance = {}
# parcours_dot(tree3, existance)
# fichier = open("graphe.dot", 'a')
# fichier.write("}")
# fichier.close()
# os.system("dot -Tsvg graphe.dot -o ./Test2.svg")