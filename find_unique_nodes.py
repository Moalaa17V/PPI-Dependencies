import pandas as pd

def find_unique_nodes(ppi_file)

myfile =r'E:\Mohamed_R\Python_project\Script\PathLinker_2018_human-ppi-weighted-cap0_75.txt'
df = pd.read_csv(myfile, sep='\t',header=(0))

a = df['#tail'].append(df['head']).unique()
print(a)
