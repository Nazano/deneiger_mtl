import networkx as nx


def solve(num_vertices, edge_list):
    """
    Fonctions Solve pour le cas de la déneigeuse

    Cette fonction prend un liste de plusieurs vertices et après l'avoir convertit en un Graph
    on tente de calculer un circuit eulérien pour définir le parcours de la dénéigeuse. Pour le
    moment le Graph en entrée que n'etre que dirigé.

    Args:
        num_vertices (int): Indique le nb de noeuds dans le Graph
        edge_list (List): List composé de tuple3 dans le format suivant : 
                            [(Node1, Node2, Weight), (Node2,Node3, Weight), ..., (NodeN, NodeN+1, Weight)]

    Raises:
        nx.NetworkXError: Si le graph est n'est pas connecté et ni faiblement connecté
                            la bibliothèque va lever une erreur pour nous l'indiquer

    Returns:
        Tuple2: Il s'agit d'un tuple avec 2 composantes la 1ère représente le nombre de vertices dans le graph traité,
                et la 2nd est le circuit eulérien retourné par le fonction solve. Représentant le chemin a suivre par
                la dénéigeuse.
    """
    # On Convertit l'edge_list en un Graph pour le traité plus facilement avec la bibilothèque Networkx
    G = nx.Graph()
    for u, v, w in edge_list:
        G.add_edge(u, v, weight=w)

    # Une fois le graph obtenu on verifie si il est dirigé si il est le cas on verifie si il est faiblement connecté
    if G.is_directed() and not nx.is_weakly_connected(G):
        raise nx.NetworkXError("G is not connected")
    # Une fois le graph obtenu on verifie si il est dirigé si il est le cas on verifie si il est connecté
    if not G.is_directed() and not nx.is_connected(G):
        raise nx.NetworkXError("G is not connected")

    circuit = []
    # Si le graph est eulerien on peut calculer directement le circuit
    if nx.is_eulerian(G):
        circuit = [i for i in nx.eulerian_circuit(G)]

    # Si le graph n'est pas eulerien on cherche a le rendre eulérien puis on peut calculer directement
    # le circuit depuis le graph résultat qui sera eulérien
    else:
        # Cette fonction Peut lever une erreur si G ne peut pas etre rendu eulérien
        G = nx.algorithms.euler.eulerize(G)
        circuit = [i for i in nx.eulerian_circuit(G)]
    return num_vertices, circuit