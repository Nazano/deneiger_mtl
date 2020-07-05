"""
Résolution du chemin du drone via le problème du postier chinois
"""

import osmnx as ox
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from animation import animate

def min_distance_paires(G, noeud_degres_impair):
      
    paires = combinations(noeud_degres_impair, 2)
    paires_distance_min = plus_court_chemin(G, paires)
    G_complet = creer_graphe_complet(paires_distance_min)
    couplage = trouver_couplage_minimal(G_complet)
    G_augmentant = ajout_chemin_augmentant(G, couplage)
    G_augmentant = nx.eulerize(G_augmentant)
    return G_augmentant

"""
Calcule le plus court chemin pour chaque pair de sommets
"""
def plus_court_chemin(G, paires):
    dist = {}
    for paire in paires:
        dist[paire] = nx.dijkstra_path_length(G, paire[0], paire[1], weight='length')
    return dist

def creer_graphe_complet(paires_distance):
    G = nx.Graph()
    for pair, d in paires_distance.items():
        G.add_edge(pair[0], pair[1], **{'weight' : -d, 'distance' : d})
    return G

def trouver_couplage_minimal(G_complet):
    couplage = dict(nx.algorithms.max_weight_matching(G_complet, True))
    couplage_unique = list(pd.unique([tuple(sorted([k, v])) for k, v in couplage.items()]))
    return couplage_unique

def ajout_chemin_augmentant(G, arretes):
    G_augmentant = nx.Graph(G.copy())
    for arrete in arretes:
        G_augmentant.add_edge(arrete[0], arrete[1],\
             **{'length': nx.dijkstra_path_length(G, arrete[0], arrete[1], weight='length'),\
                'type': 'augmented'})
    return G_augmentant

def afficher_graphe(G, positons_sommets, couplage):
    plt.figure(figsize=(8, 6))
    plt.axis('off')
    plt.title(f'Graphe complet')
    nx.draw_networkx_nodes(G, positons_sommets, node_size=16, node_color="red")
    nx.draw_networkx_edges(G, positons_sommets, alpha=0.6)
    g_odd_complete_min_edges = nx.Graph(couplage)
    nx.draw(g_odd_complete_min_edges, pos=positons_sommets, node_size=20, edge_color='blue', node_color='red')
    plt.show()

def statistiques(eulerian_circuit, vitesse_moy = 30):
    distance_parcourue = sum([a[2] for a in eulerian_circuit])
    temps = distance_parcourue / (1000 * vitesse_moy)
    print(f'distance_parcourue: {round(distance_parcourue / 1000, 2)}km')
    print(f'temps estimé: {round(temps, 2)}h à une vitesse de {vitesse_moy}km/h')

def drone_path(file, stats = True, animation = False, animation_folder = "/tmp"):
    print("Chargement du fichier...")
    G = ox.load_graphml(file).to_undirected()
    print("Fichier chargé")
    print("Traitement...")
    poistion_des_sommets =\
        { s : p for s, p in zip(G.nodes, zip(dict(G.nodes.data('x')).values(), dict(G.nodes.data('y')).values())) }    
    noeud_degres_impair = [s for s, d in G.degree() if d % 2 == 1]
    G_aug = min_distance_paires(G, noeud_degres_impair)
    eulerian_circuit = nx.eulerian_circuit(G_aug)
    tmp = []
    for e in eulerian_circuit:
        tmp.append((e[0], e[1], G_aug.get_edge_data(e[0], e[1])[0]['length']))
    print('OK')
    if stats:
        statistiques(tmp)
    if animation:
        print("Calcul de l'animation...")
        animate(G, G_aug, list(nx.eulerian_circuit(G_aug)), poistion_des_sommets, animation_folder, file)
        print("OK")
    return list(nx.eulerian_circuit(G_aug))