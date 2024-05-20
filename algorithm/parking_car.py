import numpy as np
from algorithm.basic_rrt import BasicRRT
from map.map import *
import math
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


from map.node import Node
import time


class ParkingCarRRT(BasicRRT):

    def __init__(self, map:ParkingMap, step_size:int):
        self.vehicle_length = 35
        self.robot_wheel_radius = 3
        self.left_rpm =25
        self.right_rpm =30
        self.map = map
        self.start_time = time.time()
        self.map.definingObstacle()
        super().__init__(self.map, step_size) 

    def possibleIncrement(self,left_wheel_rpm, right_wheel_rpm,theta):
        left_wheel_rpm = ((2*np.pi)*left_wheel_rpm)/60
        right_wheel_rpm = ((2*np.pi)*right_wheel_rpm)/60
        dt = 0.5
        dx = 0.5*self.robot_wheel_radius*(left_wheel_rpm+right_wheel_rpm)*(math.cos(theta))*dt
        dy = 0.5*self.robot_wheel_radius*(left_wheel_rpm+right_wheel_rpm)*(math.sin(theta))*dt
        dtheta = (self.robot_wheel_radius/self.vehicle_length)*(right_wheel_rpm - left_wheel_rpm)*dt
        return dx , dy , dtheta
        
        
    def move(self, left, right,selected_node):
        current_node = selected_node
        node_list = []

        for i in range(8):
            current_points = current_node.getPoints()
            current_orentation = current_node.getOrientation()

            dx , dy , dtheta = self.possibleIncrement(left,right, current_orentation)
            new_x = current_points[0] + dx
            new_y = current_points[1] + dy
            new_theta = current_orentation + dtheta
            new_points = (new_x,new_y)
            if self.map.checkObstacle(current_points,new_points):
                return
            if self.map.allObstecalePoints(new_points[0],new_points[1]):
                return
            new_node = Node(position=new_points,orientation=new_theta, parent= current_node )
            node_list.append(new_node)
            current_node = new_node

            # for n in node_list:
            #     self.map.drawLine(n.position ,n.parent.position, (139,173,60)  , 2 )

        return node_list
    
    def action1(self,node1):
        return self.move( left=0, right= self.left_rpm, selected_node= node1)

    def action2(self,node1):
        return self.move( left=self.left_rpm, right= 0, selected_node= node1)

    def action3(self,node1):
        return self.move( left=self.left_rpm, right= self.left_rpm, selected_node= node1)

    def action4(self,node1):
        return self.move( left=0, right= self.right_rpm, selected_node= node1)

    def action5(self,node1):
        return self.move( left=self.right_rpm, right= 0, selected_node= node1)

    def action6(self,node1):
        return self.move( left=self.right_rpm, right= self.right_rpm, selected_node= node1)

    def action7(self,node1):
        return self.move( left=self.left_rpm, right= self.right_rpm, selected_node= node1)

    def action8(self,node1):
        return self.move( left=self.right_rpm, right= self.left_rpm, selected_node= node1)
    

    def bestPossibleMove(self, random_point, chosen_node):
        min_distance = None
        best_node = None
        node_list = None
        for move in [self.action1, self.action2, self.action3, self.action4, self.action5, self.action6, self.action7, self.action8]:
            one_move_sub_nodes = move(chosen_node)

            if one_move_sub_nodes is not None:
                for n in one_move_sub_nodes:
                    if n :
                        if self.euclidean_distance(n.position, self.end_point) < 10:
                            return True, n

                new_node = one_move_sub_nodes[len(one_move_sub_nodes)-1]

                dr = self.euclidean_distance(new_node.position, random_point )

                if min_distance is None:
                    min_distance = dr
                    node_list = one_move_sub_nodes
                    best_node = new_node
                elif dr < min_distance :
                    min_distance= dr
                    best_node = new_node
                    node_list = one_move_sub_nodes
        
        if node_list :
            for sub_node in node_list:
                if self.euclidean_distance(sub_node.position, self.end_point) < 10:
                    print("point found")
                    return True, sub_node
                if self.map.allObstecalePoints(sub_node.position[0],sub_node.position[1]  ):
                    break
                self.map.drawLine(sub_node.position ,sub_node.parent.position, (139,173,60)  , 2 )
        
        return False , best_node
    
    def goalReached(self, node, end_node):
        if self.euclidean_distance(node.position, end_node.position) < 30:
                print("Goal Reached")
                self.path_points = self.backTrack(node )
                return True
        
    def checkParkProximity(self, current_position) :
        distance = self.euclidean_distance(current_position, self.park_point)
        if distance <= 100:
            if not self.point_changed:
                self.map.drawPoint(current_position, (165, 125, 125))
            print("Park Point Reached")
            return True
        return False
    
    def get_distance(self, p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        
    def backTrack(self, node, isparking = True):
        # Collect path points from the node to the root

        count = 0
        path = []
        while node is not None:
            path.append(node.position)
            node = node.parent


        # Smooth the path
        smooth_path = self.smoothPath(path[::-1])  # Reverse path and smooth it

        # Draw lines between consecutive points in the smoothed path
        if smooth_path.size > 0:  # Check if the smooth_path is not empty
            for i in range(len(smooth_path) - 1):  # Stop loop at the second-to-last element
                count = count +1
                if (isparking and count%150 == 0):
                    self.map.drawCircle(smooth_path[i],100, (0, 0, 255))
                self.map.drawLine(smooth_path[i], smooth_path[i+1], (255, 0, 0), 2)
        end_time = time.time() 
        total_time = end_time - self.start_time
        print(f"Total execution time: {total_time:.2f} seconds")

        return smooth_path
    
    

    
    def smoothPath(self, path, resolution=100):
  
        if not path:
            return np.array([])  # Return an empty array if path is empty

        # Extract the x and y coordinates from the path
        x = [point[0] for point in path]
        y = [point[1] for point in path]

        # Calculate the cumulative distance along the path
        distance = np.cumsum([0] + [np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2) for i in range(1, len(path))])
        distance /= distance[-1]  # Normalize to a 0-1 range

        # Create cubic splines for x and y over distance
        cs_x = CubicSpline(distance, x, bc_type='clamped')
        cs_y = CubicSpline(distance, y, bc_type='clamped')

        # Generate the smooth path at high resolution
        fine_distance = np.linspace(0, 1, len(path) * resolution)
        smooth_x = cs_x(fine_distance)
        smooth_y = cs_y(fine_distance)

        return np.vstack((smooth_x, smooth_y)).T

    

    def rrtImplemtation(self):

        end_node = Node(self.end_point, None )
        self.nodes[self.inital_node.position] = self.inital_node
        closet_node = self.inital_node

        point_changed = False
        self.point_changed = point_changed

        while True:

            if point_changed :
                end_node = Node(self.park_point, None )

            if self.euclidean_distance(closet_node.position, end_node.position) < 10:
                print("Goal Reached")
                self.path_points = self.backTrack(closet_node )
                break

                        
            if not point_changed:         
                if self.checkParkProximity(closet_node.position) :
                    self.initial_node = Node(closet_node.position, None)
                    self.start_point = closet_node.position
                    self.end_point = self.park_point
                    end_node = Node(self.park_point, None )
                    print("hello {self.end_point}")
                    point_changed = True
                    self.point_changed = point_changed
                    
                    
                    
                    self.path_points = self.backTrack(closet_node )


                    self.parkingRRt(closet_node)
                    
                    return 
            
            
            x,y = self.randomPoint()  
            closet_node = self.closetNode(x,y)

            isClose , target_node = self.bestPossibleMove((x,y),closet_node)

            if isClose :
                self.path_points = self.backTrack(closet_node )
                end_time = time.time() 
                total_time = end_time - self.start_time
                print(f"Total execution time: {total_time:.2f} seconds")
                return
                

            if target_node is None:
                continue
            self.nodes[target_node.position ] = target_node

    def parkingRRt(self,closet_node):

        end_node = Node(self.end_point, None )
        self.nodes[closet_node.position] = closet_node
        inital_node = closet_node
        

        while True:
            
            if self.euclidean_distance(closet_node.position, end_node.position) < 10:
                print("Goal Reached_4_3")
                path = []
                while closet_node.position != inital_node.position:
                    path.append(closet_node.position)
                    closet_node = closet_node.parent
                    
                for i in range(len(path) - 1):
                    self.map.drawLine(path[i], path[i+1],(255, 134, 104), 5)

                end_time = time.time() 
                total_time = end_time - self.start_time
                print(f"Total execution time: {total_time:.2f} seconds")
                    
                    
                break
            
                        
            x,y = self.randomPoint()  
            closet_node = self.closetNode(x,y)
            
            

            is_close , target_node = self.bestPossibleMove((x,y),closet_node)

            if is_close :
                print("Goal Reached_4")
                path = []
                
                while closet_node.position != inital_node.position and closet_node.position is not None: 
                    path.append(closet_node.position)
                    closet_node = closet_node.parent
                    
                for i in range(len(path) - 1):
                    self.map.drawLine(path[i], path[i+1],(225, 225, 0), 5)
                return
                
            if target_node is None:
                continue
            self.nodes[target_node.position ] = target_node

    

    