import hou
from searchtree.searchtree import Tree

def search(node):
  dataset = Tree()

  query = node.parm('query').eval()
  results = dataset.query(query)

  result_str = ''
  for res in results:
    result_str += res + '\n'

  node.parm('results').set(result_str)
    
def loadDataset(node):
  path = node.parm('data_load').eval()
  Tree.loadDataset(path)