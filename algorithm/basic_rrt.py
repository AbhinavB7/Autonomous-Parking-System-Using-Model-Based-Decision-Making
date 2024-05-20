from map.node import Node
from map.map import *
import random
import numpy as np
import time


class BasicRRT:
    def __init__(self, map:ParkingMap, step_size:int ):
        # Constants
        self.step_size = step_size
        self.goal_thershold = 10
        
        self.start_point = map.start_point
        self.end_point = map.end_point

        self.park_point = map.park_point
        self.inital_node = Node(self.start_point,parent=None)

        self.map = map
        self.map.drawParkingLots()
        
        self.nodes = dict()

        self.rrtImplemtation()
        self.map.run()


    def randomPoint(self):
        x = random.randint(10, 390)
        y = random.randint(10, 390)
        return (x, y)
    
    
    def normalizeVector(self, start_point, end_point):
        vector = np.array([end_point[0] - start_point[0], end_point[1] - start_point[1]])
        norm = np.linalg.norm(vector)
        if norm == 0:  
            return  None
        return  (vector / norm)
    

    
    def euclidean_distance(self,p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    

    def closetNode(self,x,y): 
        closet_node = None
        for position, node in self.nodes.items():
            if closet_node is None:
                closet_node = node
                continue
            if self.euclidean_distance(position, (x,y)) < self.euclidean_distance(closet_node.position, (x,y)):
                closet_node = node
        return closet_node
    
    def checkParkProximity(self, current_position) :
        # closet_node = self.closetNode(current_position[0],current_position[1])
        distance = self.euclidean_distance(current_position, self.park_point)
        return distance <= 30
    
    
    def backTrack(self, node):
        path = []
        while node is not None:
            path.append(node.position)
            node = node.parent
            
        for i in range(len(path) - 1):
            self.map.drawLine(path[i], path[i+1],(255, 0, 0), 2)
        return path[::-1]
         
    
    def rrtImplemtation(self):

        end_node = Node(self.end_point, None )

        self.nodes[self.inital_node.position] = self.inital_node

        
        closet_node = self.inital_node
        while True:
            if self.euclidean_distance(closet_node.position, end_node.position) < 20:
                print("Goal Reached")
                self.backTrack(closet_node )
                break
            
            
            x,y = self.randomPoint()
            
            closet_node = self.closetNode(x,y)

            
            unit_vec = self.normalizeVector(closet_node.position, (x,y) ) *(self.step_size)
            new_position = (closet_node.position[0] + unit_vec[0], closet_node.position[1] + unit_vec[1])

            if self.map.isObstacle(closet_node.position,unit_vec):
                continue
    
            if unit_vec is None:
                return
            self.map.drawVector(closet_node.position, unit_vec )
            self.map.drawPoint(closet_node.position , (182, 83, 195))
            self.nodes[new_position] = Node(new_position, closet_node)
            
            