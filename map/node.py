class Node:
    def __init__(self, position, parent,orientation = 0) :
        self.position = position
        self.parent = parent
        self.orientation = orientation
        self.children = [] 

    def getPoints(self):
        return self.position
    
    # Orientation of the Node
    def getOrientation(self):
        return self.orientation
    
    # Parent Node
    def getParent(self):
        return self.parent
    
    def __eq__(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

    def __hash__ (self):
        return hash((self.position[0], self.position[1]))