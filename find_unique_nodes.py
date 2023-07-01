import pandas as pd

def find_unique_nodes(ppi_file):

    myfile = ppi_file
    df = pd.read_csv(myfile, sep='\t',header=(0))
    a = df['#tail'].append(df['head']).nunique()
    print(a)
    
    return find_unique_nodes
