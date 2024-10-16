import numpy
import pickle
import pandas
import os.path

class TreeNode():
  
  def __init__(self, value) -> None:
    self.value = value
    self.children = {}

  def __format__(self, __format_spec: str) -> str:
    return 'value: {0}'.format(self.value)

class Tree():

  dumpfile = 'tree_dump.pkl'
  
  def __init__(self) -> None:
    self.output = None

    if os.path.exists(Tree.dumpfile):
      with open(Tree.dumpfile, 'rb') as file:
        self.root = pickle.load(file)
    else:
      self.root = TreeNode('')

  def __format__(self, __format_spec: str) -> str:
    self.output = []
    self._dfs(self.root, '')
    return '{}'.format(self.output)

  def insert(self, value: str) -> None:
    cur = self.root
    for c in value:
      if len(cur.children) == 0 or c not in cur.children.keys():
        cur.children[c] = TreeNode(c)
      cur = cur.children[c]

  def query(self, value) -> numpy.ndarray:
    st = self._searchSubtree(self.root, value)

    self.output = []
    if st is not None:
      self._dfs(st, value[:-1])

    return numpy.array(self.output)

  def dump(self) -> None:
    with open(Tree.dumpfile, 'wb') as file:
      pickle.dump(self.root, file)
  
  @staticmethod
  def loadDataset(datapath) -> None:
    print(datapath)
    if os.path.exists(datapath):
      data = pandas.read_csv(datapath)
    
      tree = Tree()
      for e in data['Title']:
        tree.insert(e)
      tree.dump()
    else:
      print('Dataset not found: {0}'.format(datapath))

  def _searchSubtree(self, node: TreeNode, value: str) -> TreeNode:
    if len(node.children) == 0 and len(value) > 0:
      return None
    
    cur = self.root
    for c in value:
      if c not in cur.children.keys():
        return None
      
      cur = cur.children[c]

    return cur

  def _dfs(self, node: TreeNode, prefix: str) -> str:
    res = '{0}{1}'.format(prefix, node.value)
    if len(node.children) == 0:
      self.output.append(res)
    else:
      for child in node.children.values():
        self._dfs(child, res)

if __name__ == '__main__':
  datapath = os.path.join(os.path.basename(__file__), 'MoviesOnStreamingPlatforms.csv')
  Tree.loadDataset(datapath)

  data = Tree()
  res = data.query('The')
  print('{}'.format(res))