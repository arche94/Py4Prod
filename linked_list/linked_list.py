import hou

def init_list(n):
  ctx = hou.node('/obj').createNode('geo')

  if (n == 0):
    return None

  root = ctx.createNode('null', 'node_{0}'.format(len(ctx.children())))
  
  cur = root
  while len(ctx.children()) < n:
    cur = cur.createOutputNode('null', 'node_{0}'.format(len(ctx.children())))

  ctx.layoutChildren()

  return root

def insert_at(root, new_node, parent_name):
  if parent_name == None:
    root.setInput(0, new_node)
    root.parent().layoutChildren()
    return new_node

  cur = root  
  while cur is not None:
    if cur.name() == parent_name:
      if len(cur.outputs()) > 0:
        cur.outputs()[0].setFirstInput(new_node)
      new_node.setFirstInput(cur)
      cur.parent().layoutChildren()
      return root
    cur = cur.outputs()[0] if len(cur.outputs()) > 0 else None
  
  print('Parent node not found')

def find_tail(root):
  while len(root.outputs()) > 0:
    root = root.outputs()[0]
  return root

def print_list(root):
  while root is not None:
    print(root.name())
    root = root.outputs()[0] if len(root.outputs()) > 0 else None

def test():
  for node in hou.node('/obj').children():
    node.destroy()

  print('========= Init list =========')
  head = init_list(13)
  print_list(head)
  print()
  
  print('========= Tail =========')
  tail = find_tail(head)
  print(tail.name())
  print()

  print('========= Insert =========')
  ctx = hou.node('/obj').children()[0]
  new_node_0 = ctx.createNode('null', 'new_node_{0}'.format(len(ctx.children())))
  new_node_1 = ctx.createNode('null', 'new_node_{0}'.format(len(ctx.children())))
  new_node_2 = ctx.createNode('null', 'new_node_{0}'.format(len(ctx.children())))

  print('--- Insert in the middle')
  head = insert_at(head, new_node_0, 'node_9')
  print_list(head)
  print()

  print('--- Insert at the end')
  head = insert_at(head, new_node_1, find_tail(head).name())
  print_list(head)
  print()
  print('-> New tail')
  tail = find_tail(head)
  print(tail.name())
  print()

  print('--- Insert at the head')
  head = insert_at(head, new_node_2, None)
  print_list(head)
  print()
  
  print('-> New head')
  print(head.name())
  print()

