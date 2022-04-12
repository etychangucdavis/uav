from asyncio.windows_events import NULL
import numpy as np
import pandas as pd
import math
from DefineNode import Node_defer as Node

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

  # 更新每個點的鄰居表
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
                # 鄰居為黑色節點，也加入至黑鄰居表中
                elif other_node.color > 0:
                    node.SetBlackNeighborList(other_node)

                # 並更新該鄰居的鄰居表
                other_node.SetNeighborList(node)
                # 該點為白色節點，也加入至白鄰居表中
                if not node.color :
                    other_node.SetWhiteNeighborList(node)
                # 該點為黑色節點，也加入至黑鄰居表中
                elif node.color > 0:
                    other_node.SetBlackNeighborList(node)
        # 此節點為黑色節點且有白鄰居則加進B'中
        if node.color and len(node.neighbor_w_list):
          self.B_.append(node)    

  # 判斷當前黑色節點是否存在任一白色鄰居
  def CheckWhiteNeighbor(self):
    for node in self.B_:
      if node.GetWhiteNeighborList():
        return True
    return False

  # 執行演算法
  def RunGreedy(self):
    # start from line 5 
    iters = 1
    while(self.CheckWhiteNeighbor()):
      B = self.B_
      # Candidate set
      self.C = []
      # 回傳self.C之前將染黑的節點染回白色
      backtoWhite = []
      for node in B:
        w_list = node.GetWhiteNeighborList()
        self.R += [w_x for w_x in w_list if w_x not in self.R]
      while self.R :
        max_neighbor = -1
        # argmax|w(x)|
        for node in B:
          if len(node.GetWhiteNeighborList()) > max_neighbor:
            max_neighbor = len(node.GetWhiteNeighborList())
            x = node
        # C = C Union {x}
        self.C.append(x)
        # B = B - {x}
        B = [node for node in B if node is not x]
        # color nodes in w(x) as black ，最後要染回白色
        w_x = x.GetWhiteNeighborList()
        for node in w_x:
          node.ToBlack_greedy()
          backtoWhite.append(node)
        # R = R - w(x)
        self.R = [ _ for _ in self.R if _ not in w_x]
        # B' = B' Union w(x)
        self.B_ += [ _ for _ in w_x if _ not in self.B_]
      print(f' -----Greedy {iters}th-----')  
      iters += 1
      for node in self.C:
        node.PrintContent()
      for node in backtoWhite:
        node.ToWhite_greedy()
      yield self.C 
    yield NULL

  # 執行 Defer演算法
  def RunDefer(self):
    defer = self.RunGreedy()
    iters = 1
    while 1:
      every_round = []
      # 用來存放所有被染灰的節點，在最後通通染黑
      toGrayList = []
      # line 1
      C = next(defer)
      if not C:
        return self.S
      # line 2
      while C :
        # 最小的白鄰居數
        min_neighbor = 1000
        # argmin|w(x)|
        for node in C:
          if len(node.GetWhiteNeighborList()) < min_neighbor:
            min_neighbor = len(node.GetWhiteNeighborList())
            x_hat = node
            T =  x_hat.GetWhiteNeighborList()
        # line 3
        for node in T:
          # line 4
          other_blacklist = node.GetBlackNeighborList()
          other_blacklist = [ _ for _ in other_blacklist if _ is not x_hat and _ in C]
          if other_blacklist :
            continue
          # line 5
          if node.GetGrayNeighborList():
            # line 6
            # any_exit變數用來判斷是否存在一個節點r滿足"沒有其他灰或黑鄰居"的條件
            any_exit = 0
            w_n = node.GetWhiteNeighborList()
            # 若該白色節點皆無任何一個灰色或黑色鄰居節點，則做line 7的動作
            for r in w_n:
              other_blackList = r.GetBlackNeighborList()
              # 除了 x_hat 以外其他的黑色鄰居
              other_blackList = [ _ for _ in other_blackList if _ is not x_hat and _ in C]
              if not other_blackList and not r.GetGrayNeighborList():
                any_exit += 1
            # 周圍都是灰色鄰居或其他黑色鄰居
            if not any_exit:
              continue
          # line 7
          # color nodes in w(x) as gray
          w_x = x_hat.GetWhiteNeighborList()
          for node_ in w_x:
            node_.ToGray()
            toGrayList.append(node_)
          # S := S Union {x_hat}
          self.S.append(x_hat)
          every_round.append(x_hat)
          break # go to line 2
        # Remove x_hat in C
        C = [node for node in C if node is not x_hat]
      # 做Greedy前，將所有被染灰的節點都染黑
      for node in toGrayList:
        node.ToBlack()
      print(f' -----Defer {iters}th-----')  
      iters += 1
      for node in every_round:
        node.PrintContent()

# 計算兩點之間的距離
def ComputeDistance(x, y):
    return math.hypot(x, y)

test = Topology(mode='square_four', radius=math.sqrt(2))
test.UpdateNeighbor()

s = test.RunDefer()

print("Defer result :")
for node in s:
   node.PrintContent()