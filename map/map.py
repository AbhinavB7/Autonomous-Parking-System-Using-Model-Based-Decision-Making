import pygame
import math
import sys
from pygame.locals import *
from map.point import Point
import random

class ParkingMap:
    def __init__(self, start_point, end_point, park_point):
        self.start_point = start_point
        self.end_point = end_point
        self.park_point = park_point
        self.canvas_width = 420
        self.canvas_height = 420
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.canvas_width, self.canvas_height))
        pygame.display.set_caption("Parking Map Simulation")

        # Colors
        self.blue_color = (255, 255, 0)  # Yellow
        self.green_color = (0, 255, 0)   # Green
        self.red_color = (255, 0, 0)     # Red
        self.line_color = (139,173,60) 
        self.goal_color = (0, 0, 255)     # Blue

        # Draw the parking lot and update the display
        self.drawParkingLots()
        self.startEndPoint(self.start_point, self.end_point, self.park_point)
        pygame.display.flip()

    def onSegment(self, p, q, r): 
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
            return True
        return False

    def orientation(self, p, q, r):     
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
        if (val > 0): 
            return 1
        elif (val < 0): 
            return 2
        else: 
            return 0
 
    def doIntersect(self, p1,q1,p2,q2): 
        o1 = self.orientation(p1, q1, p2) 
        o2 = self.orientation(p1, q1, q2) 
        o3 = self.orientation(p2, q2, p1) 
        o4 = self.orientation(p2, q2, q1) 


        if ((o1 != o2) and (o3 != o4)): 
            return True

        if ((o1 == 0) and self.onSegment(p1, p2, q1)): 
            return True

        if ((o2 == 0) and self.onSegment(p1, q2, q1)): 
            return True

        if ((o3 == 0) and self.onSegment(p2, p1, q2)): 
            return True

        if ((o4 == 0) and self.onSegment(p2, q1, q2)): 
            return True
    
        return False


    def drawLine(self, start, end, color, width):
        pygame.draw.line(self.screen, color, start, end, width)
        pygame.display.update()

    def drawRectangle(self, x, y, width, height, color, alpha=255):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.display.update()
        
    def drawCircle(self, position, radius, color):
        pygame.draw.circle(self.screen, color, position, radius, width=1)
        pygame.display.update()

    def addObstacle(self, top_left_x, top_left_y, color):
        pygame.draw.rect(self.screen, color, (top_left_x, top_left_y, 40, 40))

    def startEndPoint(self, start_point, end_point, park_point):
        pygame.draw.rect(self.screen, self.green_color, (start_point[0], start_point[1], 10, 10))
        pygame.draw.rect(self.screen, self.red_color, (end_point[0], end_point[1], 10, 10))
        pygame.draw.rect(self.screen, self.goal_color, (park_point[0], park_point[1], 10, 10))
        # pygame.draw,rect(self)
        color = self.screen.get_at(end_point)
        print(f"color at {end_point} is {color}")

    def drawParkingLots(self):
        # Draw vertical lines
        self.drawLine((100, 100), (100, 300), self.blue_color, 2)
        self.drawLine((300, 100), (300, 300), self.blue_color, 2)
        self.drawLine((400, 100), (400, 300), self.blue_color, 2)

        # Draw horizontal lines
        # self.drawLine((0, 100), (100, 100), self.blue_color, 10)
        # self.drawLine((0, 300), (100, 300), self.blue_color, 10)
        # self.drawLine((300,100), (420,100), self.blue_color, 10)
        # self.drawLine((300,300), (420,300), self.blue_color, 10)

        self.hor_line = []
        hor0 = [(0, 100), (100, 100)]
        hor_0 = [(0, 300), (100, 300)]
        # hor_r = [(300,100), (420,100)]
        # hor_r1 = [(300,300), (420,300)]
        self.hor_line.append(hor0)
        self.hor_line.append(hor_0)
        # self.hor_line.append(hor_r)
        # self.hor_line.append(hor_r1)
        for i in range(5):
            y = 100 + i * 50
            hor1 = [(100, y), (150, y)]
            hor2 = [(250, y), (300, y)]
            self.hor_line .append(hor1)
            self.hor_line .append(hor2)
            self.drawLine((100, y), (150, y), self.blue_color, 2)
            self.drawLine((250, y), (300, y), self.blue_color, 2)
          

        # Draw angled lines
        for j in range(5):
            x = 400
            y = 100 + j * 50
            end_x = x - 50 
            end_y = y 
            hor3 = [(x, y), (end_x, end_y)]
            self.hor_line.append(hor3)
            self.drawLine((x, y), (end_x, end_y), self.blue_color, 2)

    # def isTolerance(self, point):
    #     # Define the tolerance in pixels
    #     tolerance = 10

    #     # Check vertical lines
    #     vertical_lines = [(100, 100, 300), (300, 100, 300), (400, 100, 250)]
    #     for x, y_start, y_end in vertical_lines:
    #         if x - tolerance <= point[0] <= x + tolerance and y_start - tolerance <= point[1] <= y_end + tolerance:
    #             return True

    #     # Check horizontal lines
    #     horizontal_lines = []
    #     for i in range(5):
    #         y = 100 + i * 50
    #         horizontal_lines.extend([(100, 150, y), (250, 300, y)])
        
    #     for x_start, x_end, y in horizontal_lines:
    #         if x_start - tolerance <= point[0] <= x_end + tolerance and y - tolerance <= point[1] <= y + tolerance:
    #             return True

    #     return False


    def drawPoint(self, position, color):
        radius = 5  
        pygame.draw.circle(self.screen, color, position, radius)
        pygame.display.update()

    def checkObstacle(self, start_pos, end_pos):
        # end_pos = (start_pos[0] + vector[0], start_pos[1] + vector[1])
        if self.doIntersect(Point((100, 100)), Point((100, 300)),Point(start_pos), Point(end_pos)) or self.doIntersect(Point((300, 100)), Point((300, 300)),Point(start_pos), Point(end_pos)) or self.doIntersect(Point((400, 100)), Point((400, 300)),Point(start_pos), Point(end_pos)) :
            return True
        elif self.outOfBounds(end_pos):
            return True
        else:
            for line in self.hor_line:
                if self.doIntersect(Point(line[0]), Point(line[1]),Point(start_pos), Point(end_pos)) :
                    return True
            return False
        
    def outOfBounds(self, point):
        if point[0] < 0 or point[0] > self.canvas_width or point[1] < 0 or point[1] > self.canvas_height:
            return True
        return False

        

    def isObstacle(self, start_pos, vector):
        end_pos = (start_pos[0] + vector[0], start_pos[1] + vector[1])
        if self.doIntersect(Point((100, 100)), Point((100, 300)),Point(start_pos), Point(end_pos)) or self.doIntersect(Point((300, 100)), Point((300, 300)),Point(start_pos), Point(end_pos)) or self.doIntersect(Point((400, 100)), Point((400, 250)),Point(start_pos), Point(end_pos)) :
            return True
        else:
            for line in self.hor_line:
                if self.doIntersect(Point(line[0]), Point(line[1]),Point(start_pos), Point(end_pos)) :
                    return True
            return False
        
    def drawVectorLine(self, start_pos, end_pos):
        self.drawLine((start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]), self.line_color, 1)
        self.updateMap()

    def drawVector(self, start_pos, vector):
        end_pos = (start_pos[0] + vector[0], start_pos[1] + vector[1])
        self.drawLine((start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]), self.line_color, 1)
        self.updateMap()

    
    def updateMap(self):
        pygame.display.update()  
        pygame.time.wait(10)   

    def allowExit(self):
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")      

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()
        sys.exit()

    def is_point_in_rectangle(self, top_x, top_y, px, py):
        length = 40
        breadth = 40
        bottom_x = top_x + length
        bottom_y = top_y + breadth

        if top_x <= px <= bottom_x and top_y <= py <= bottom_y:
            return True
        else:
            return False

    def definingObstacle(self):
        self.all_obstacles = []
        for i in range(4):
            y = 105 + i * 50
            point1= [105,y]
            point2 = [255,y]
            self.all_obstacles.append(point1)
            self.all_obstacles.append(point2)
            # self.addObstacle(105,y,self.blue_color)
            # self.addObstacle(255,y,self.blue_color)
        # self.gettingRandomObs()
        
        self.right_obstacles = []
        for i in range(4):
            y = 105 + i * 50
            point1= [355,y]
            point2 = [445,y]
            self.right_obstacles.append(point1)
            self.right_obstacles.append(point2)
            # self.addObstacle(255,y,self.blue_color)
            # self.addObstacle(405,y,self.blue_color)

        self.addObstacle(self.all_obstacles[1][0],self.all_obstacles[1][1] ,self.blue_color)
        if self.park_point != (125,225):
            self.addObstacle(self.all_obstacles[4][0],self.all_obstacles[4][1] ,self.blue_color)
        self.addObstacle(self.all_obstacles[7][0],self.all_obstacles[7][1] ,self.blue_color)
        self.addObstacle(self.all_obstacles[6][0],self.all_obstacles[6][1] ,self.blue_color)
        self.addObstacle(self.all_obstacles[2][0],self.all_obstacles[2][1] ,self.blue_color)
        self.addObstacle(self.all_obstacles[3][0],self.all_obstacles[3][1] ,self.blue_color)
        self.addObstacle(self.all_obstacles[5][0],self.all_obstacles[5][1] ,self.blue_color)
        if self.park_point != (125, 125):
            self.addObstacle(self.all_obstacles[0][0],self.all_obstacles[0][1] ,self.blue_color)

        self.addObstacle(self.right_obstacles[0][0],self.right_obstacles[0][1] ,self.blue_color) #first
        self.addObstacle(self.right_obstacles[4][0],self.right_obstacles[4][1] ,self.blue_color) #third
        self.addObstacle(self.right_obstacles[2][0],self.right_obstacles[2][1] ,self.blue_color) #second
        if self.park_point !=(365,270):
            self.addObstacle(self.right_obstacles[6][0],self.right_obstacles[6][1] ,self.blue_color) #last

    def allObstecalePoints(self,px,py):
        lis = []
        skip =0
        # x = True
        if self.park_point == (125, 125):
            skip =0
        elif self.park_point == (125,225):
            skip  = 4
        elif self.park_point == (365,270):
            skip =6
        
        
        for i in range(8):
            if i ==skip and self.park_point != (365,270):
                continue
            lis.append(i)
            if self.is_point_in_rectangle(self.all_obstacles[i][0],self.all_obstacles[i][1],px,py ):
                return True
            if i ==skip and self.park_point == (365,270):
                continue
            if self.is_point_in_rectangle(self.right_obstacles[i][0],self.right_obstacles[i][1],px,py ):
                return True
            
        # for j in range(8):
        #     if self.is_point_in_rectangle(self.right_obstacles[i][0],self.right_obstacles[i][1],px,py ):
        #         return True

        return False
    
    def drawCircle(self, position, radius, color):
        pygame.draw.circle(self.screen, color, position, radius, width=1)
        pygame.display.update()
        





    # def get_four_random_index(self):
    #     return [random.randint(0, 7) for _ in range(4)]
    
    # def gettingRandomObs(self):
    #     random_values = self.get_four_random_index()

        # for r in random_values:
        #     self.addObstacle(self.all_obstacles[r][0],self.all_obstacles[r][1] ,self.blue_color)




    

