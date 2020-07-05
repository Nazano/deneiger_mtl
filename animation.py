import networkx as nx
import glob
import numpy as np
import imageio
import os
import matplotlib.pyplot as plt
import copy
import osmnx as ox
from pygifsicle import optimize

def animate(G_original, graph, euler_circuit, positons_sommets, animation_folder, address : str):
    faddress = address.replace(" ", "") 
    if not os.path.exists(f"{animation_folder}/{faddress}"):
        os.mkdir(f"{animation_folder}/{faddress}")
    for cpt in range(len(euler_circuit)):
        G = nx.Graph(euler_circuit[:cpt])
        ox.plot_graph(G_original, show=False, close=False, edge_alpha=0.5)
        plt.title(f"Survol du réseau routier\n{address}")
        nx.draw_networkx_nodes(G, pos=positons_sommets, node_size=6, alpha=0.6, node_color='lightgray', with_labels=False, linewidths=0.1)
        nx.draw_networkx_edges(G, pos=positons_sommets, edge_color='blue', alpha=0.9, style='dashed')
        plt.axis('off')
        plt.savefig(f'{animation_folder}/{faddress}/img{cpt}.png', dpi=80, bbox_inches='tight')
        plt.close()
    make_circuit_video(f'{animation_folder}/{faddress}/', f'drone_{faddress}.gif', fps=25)


def make_circuit_video(image_path, movie_filename, fps=5):
    # sorting filenames in order
    filenames = glob.glob(image_path + 'img*.png')
    filenames_sort_indices = np.argsort([int(os.path.basename(filename).split('.')[0][3:]) for filename in filenames])
    filenames = [filenames[i] for i in filenames_sort_indices]

    # make movie
    with imageio.get_writer(movie_filename, mode='I', fps=fps) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    optimize(movie_filename)