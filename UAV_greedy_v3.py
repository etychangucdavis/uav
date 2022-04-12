import numpy as np
import pandas as pd
import math
class Node:
  def __init__(self, id, x=0, y=0, color=0):
    self.color = color # 0:white 1:black
    self.id = id
    self.x = x
    self.y = y
    self.neighbor_w_list = [] # 白鄰居表
    self.neighbor_list = [] # 鄰居表

  # 染黑此節點，並更新周圍鄰居的白鄰居表
  def ToBlack(self):
    self.color = 1
    for node in self.neighbor_list:
      node.DeleteNeighbor(self)

  # 設置白鄰居列表
  def SetWhiteNeighborList(self, white_neighbor):
    self.neighbor_w_list.append(white_neighbor)

  # 設置鄰居列表
  def SetNeighborList(self, neighbor):
    self.neighbor_list.append(neighbor)

  # 取得白鄰居列表
  def GetWhiteNeighborList(self):
    return self.neighbor_w_list

  # 刪除某個鄰居
  def DeleteNeighbor(self, node_toBlack):
    self.neighbor_w_list = [ _ for _ in self.neighbor_w_list if _ is not node_toBlack]

  # 印出資訊
  def PrintContent(self):
      print(f' ID : {self.id} , x : {self.x}, y : {self.y}, color : {"Black" if self.color else "White"}')

class Topology:
  '''
  mode : 拓樸類別
  radius : 黑色節點廣播範圍
  '''
  def __init__(self, mode='square_four', radius=2):
    self.mode = mode
    self.radius = radius
    self.nodes = []
    self.S = []
    self.R = [] # remain
    # 讀取csv
    nodes = pd.read_csv(mode +'.csv')
    nodes = nodes.values.tolist()
    # 紀錄所有節點資訊的list
    for node in nodes:
        id, x, y, color = node
        self.nodes.append(Node(int(id), x, y, int(color)))

  # 初始化每個點的白鄰居表與鄰居表
  def UpdateNeighbor(self):
    self.B_ = [] # black nodes
    for i, node in enumerate(self.nodes):
        for other_node in self.nodes[i+1:]:
            if ComputeDistance(node.x-other_node.x, node.y-other_node.y) <= self.radius:
                # 加入此鄰居至鄰居表中
                node.SetNeighborList(other_node)
                # 鄰居為白色節點，也加入至白鄰居表中
                if not other_node.color :
                    node.SetWhiteNeighborList(other_node)
                # 同時更新該鄰居節點的鄰居表
                other_node.SetNeighborList(node)
                if not node.color :
                    other_node.SetWhiteNeighborList(node)
        # 此節點為黑色節點且有白鄰居則加進B'中
        if node.color and len(node.neighbor_w_list):
            #node.PrintContent()
            self.B_.append(node)    

  # 判斷當前黑色節點是否存在任一白色鄰居
  def CheckWhiteNeighbor(self):
    for node in self.B_:
      if len(node.GetWhiteNeighborList()):
        return True
    return False

  # 執行演算法
  def RunGreedy(self):
    # start from line 5 
    while(self.CheckWhiteNeighbor()):
      B = self.B_
      self.B_ = []
      for node in B:
        w_list = node.GetWhiteNeighborList()
        self.R += [w_x for w_x in w_list if w_x not in self.R]
      while self.R :
        max_neighbor = -1
        # argmax|w(x)|
        for node in B:
          #if node.neighbor_w_num > max_neighbor:
          if len(node.GetWhiteNeighborList()) > max_neighbor:
            max_neighbor = len(node.GetWhiteNeighborList())
            x = node
        # S = S Union {x}
        self.S.append(x)
        # B = B - {x}
        B = [node for node in B if node is not x]
        # color nodes in w(x) as black
        w_x = x.GetWhiteNeighborList()
        for node in w_x:
          node.ToBlack()
        # R = R - w(x)
        self.R = [ _ for _ in self.R if _ not in w_x]
        # B' = B' Union w(x)
        self.B_ += [ _ for _ in w_x if _ not in self.B_]

    return self.S

# 計算兩點之間的距離
def ComputeDistance(x, y):
    return math.hypot(x, y)

test = Topology(mode='triangle', radius=1)
test.UpdateNeighbor()
s = test.RunGreedy()

for node in s:
   node.PrintContent()