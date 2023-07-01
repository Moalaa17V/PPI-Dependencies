import networkx as nx
import matplotlib.pyplot as plt
import requests

def edge_weight_dic(start_protein, end_protein, G):
    edge_weight_dictionary = {}
    for tail, head in G.edges():
        edge_data = G.get_edge_data(tail, head)
        edge_weight = edge_data.get('edge_weight', 1)
        edge_weight_dictionary[(tail, head)] = edge_weight
    return edge_weight_dictionary

def find_shortest_paths(start_protein, end_protein, edge_weight, G):
    shortest_paths = []
    for path in nx.all_shortest_paths(G, start_protein, end_protein, weight=edge_weight):
        # Check if the path is acyclic
        if len(path) == len(set(path)):
            path_score = sum(G[u][v][edge_weight] for u, v in zip(path[:-1], path[1:]))
            path_weights = [G[u][v][edge_weight] for u, v in zip(path[:-1], path[1:])]
            shortest_paths.append((path, path_score, path_weights))
    return shortest_paths

def find_directly_connected_proteins(protein, G):
    connected_proteins = []
    
    for successor in G.successors(protein):
        weight = G[protein][successor]['edge_weight']
        connected_proteins.append((successor, weight))
    
    return connected_proteins

def analyze_protein_degrees(protein_degrees, G, histogram_output_file, rank_output_file):
    
    degrees = []
    
    for i in protein_degrees:
        degree = G.degree(i)
        degrees.append((i, degree))
            
    # Draw histogram
    plt.hist([degree for _, degree in degrees], bins=20, edgecolor='black')
    plt.xlabel('Degree')
    plt.ylabel('Count')
    plt.title('Protein Degree Histogram')
    plt.savefig(histogram_output_file,dpi=500)  # Save the histogram as an image file
    plt.close()  # Close the figure
    
    sorted_degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
    with open(rank_output_file, 'w') as output:
        for i, (protein, degree) in enumerate(sorted_degrees):
            output.write(f"Rank {i+1}: Protein {protein} | Degree: {degree}\n")
    
    
def get_gene_name(protein_ids, G):
    gene_names = []
    
    for protein_id in protein_ids:
        uniprot_url = f"https://rest.uniprot.org/uniprotkb/{protein_id}.txt"
        response = requests.get(uniprot_url)

        if response.status_code == 200:
            lines = response.text.split("\n")
            for line in lines:
                if line.startswith("GN   Name="):
                    gene_name = line.split("GN   Name=")[1].split(";")[0]
                    gene_names.append(gene_name)
                    break
            else:
                gene_names.append(None)
        else:
            gene_names.append(None)

    return gene_names

def convert_to_unweighted(G, output_file):
    unweighted_graph = G.copy()
    for u, v, attrs in unweighted_graph.edges(data=True):
        attrs.pop('edge_weight', None)
    
    node_labels = unweighted_graph.nodes()
    adjacency_matrix = nx.to_numpy_matrix(unweighted_graph)
    
    # Save the adjacency matrix with labels to a file
    with open(output_file, 'w') as file:
        # Write the node labels as the first row
        file.write('\t'.join(map(str, node_labels)))
        file.write('\n')
        
        # Write the adjacency matrix
        for row in adjacency_matrix:
            file.write('\t'.join(map(str, row)))
            file.write('\n')
