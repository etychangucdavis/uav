class Node_greedy:
  def __init__(self, id, x=0, y=0, color=0):
    self.color = color # 0:white 1:black
    self.id = id
    self.x = x
    self.y = y
    self.neighbor_w_list = [] # 白鄰居表
    self.neighbor_list = [] # 總鄰居表

  # 染黑此節點，並更新周圍鄰居的白鄰居表
  def ToBlack(self):
    self.color = 1
    for node in self.neighbor_list:
      node.Delete_W_Neighbor(self)

  # 設置白鄰居列表
  def SetWhiteNeighborList(self, white_neighbor):
    self.neighbor_w_list.append(white_neighbor)

  # 設置總鄰居列表
  def SetNeighborList(self, neighbor):
    self.neighbor_list.append(neighbor)

  # 取得白鄰居列表
  def GetWhiteNeighborList(self):
    return self.neighbor_w_list

  # 刪除某個鄰居 (變黑的鄰居)
  def Delete_W_Neighbor(self, node_toBlack):
    self.neighbor_w_list = [ _ for _ in self.neighbor_w_list if _ is not node_toBlack]

  # 印出資訊
  def PrintContent(self):
      print(f' ID : {self.id} , x : {self.x}, y : {self.y}, color : {"Black" if self.color else "White"}')


class Node_defer:
  def __init__(self, id, x=0, y=0, color=0):
    self.color = color # 0:white 1:black -1:gray
    self.id = id
    self.x = x
    self.y = y
    self.neighbor_w_list = [] # 白鄰居表
    self.neighbor_g_list = [] # 灰鄰居表
    self.neighbor_b_list = [] # 黑鄰居表
    self.neighbor_list = [] # 總鄰居表

  # 染灰此節點，並更新周圍鄰居的灰鄰居表
  def ToGray(self):
    self.color = -1
    for node in self.neighbor_list:
      node.Delete_W_Neighbor(self)
      node.SetGrayNeighborList(self)

  # 染黑此節點，並更新周圍鄰居的白鄰居表與黑鄰居表
  def ToBlack(self):
    self.color = 1
    for node in self.neighbor_list:
      node.Delete_G_Neighbor(self)
      node.SetBlackNeighborList(self)

  # 設置白鄰居列表
  def SetWhiteNeighborList(self, white_neighbor):
    self.neighbor_w_list.append(white_neighbor)

  # 更新灰鄰居列表
  def SetGrayNeighborList(self, node_toGray):
    self.neighbor_g_list.append(node_toGray)

  # 更新黑鄰居列表
  def SetBlackNeighborList(self, node_toBlack):
    self.neighbor_b_list.append(node_toBlack)

  # 設置總鄰居列表
  def SetNeighborList(self, neighbor):
    self.neighbor_list.append(neighbor)

  # 取得白鄰居列表
  def GetWhiteNeighborList(self):
    return self.neighbor_w_list

  # 取得灰鄰居列表
  def GetGrayNeighborList(self):
    return self.neighbor_g_list

  # 取得黑鄰居列表
  def GetBlackNeighborList(self):
    return self.neighbor_b_list

  # 刪除某個鄰居 (變黑的鄰居)
  def Delete_W_Neighbor(self, node_toBlack):
    self.neighbor_w_list = [ _ for _ in self.neighbor_w_list if _ is not node_toBlack]

  # 刪除某個鄰居 (變灰的鄰居)
  def Delete_G_Neighbor(self, node_toGray):
    self.neighbor_g_list = [ _ for _ in self.neighbor_g_list if _ is not node_toGray]

  # 印出資訊
  def PrintContent(self):
      print(f' ID : {self.id} , x : {self.x}, y : {self.y}, color : {"Black" if self.color else "White"}')