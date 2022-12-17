class ArbreBinaire:

  # Constructeur de la structure de donnee ArbreBinaire
  def __init__(self, valeur, id):
    self.valeur = valeur            # Etiquette du noeud
    self.enfant_gauche = None       # Enfant gauche du noeud
    self.enfant_droit = None        # Enfant droit du noeud
    self.id = id                    # Identifiant du noeud pour permettre un affichga sans doublons

  def insert_gauche(self, valeur):
    if self.enfant_gauche == None:
      self.enfant_gauche = ArbreBinaire(valeur)
    else:
      new_node = ArbreBinaire(valeur)
      new_node.enfant_gauche = self.enfant_gauche
      self.enfant_gauche = new_node

  def insert_droit(self, valeur):
    if self.enfant_droit == None:
      self.enfant_droit = ArbreBinaire(valeur)
    else:
      new_node = ArbreBinaire(valeur)
      new_node.enfant_droit = self.enfant_droit
      self.enfant_droit = new_node

  def remplace_tree(self, treeRempalacement):
    self.valeur = treeRempalacement.valeur
    self.enfant_gauche = treeRempalacement.enfant_gauche
    self.enfant_droit = treeRempalacement.enfant_droit
    self.id = treeRempalacement.id

  def get_valeur(self):
    return self.valeur

  def get_gauche(self):
    return self.enfant_gauche

  def get_droit(self):
    return self.enfant_droit

  def get_id(self):
    return self.id