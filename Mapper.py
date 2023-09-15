
import yaml

#Class Map
class Map:

    def __init__(self, numTotems, totemPoses):
        
        self.mapTotems = []

        for i in range(numTotems):
            totem = Totem()
            totem.SetTotemIdx(i)
            totem.SetPose(totemPoses['positions'][list(totemPoses['positions'])[i]])
            self.mapTotems.append(totem)

    def getSizeMap(self,):
        return len(self.mapTotems)

    def getIdxTotem(self, ID):
        for t in self.mapTotems:
            for i in range(4):
                if (t.listID[i] == ID):
                    return t.totemIdx

        return -1

    def getNextTotem(self, x,y):
        
        minDist = (((x-self.mapTotems[0].pose.x)*(x-self.mapTotems[0].pose.x)+(y-self.mapTotems[0].pose.y)*(y-self.mapTotems[0].pose.y)))**0.5
        idMinDist = 0
        
        for i in range(1,self.getSizeMap()):
            distance = (((x-self.mapTotems[i].pose.x)*(x-self.mapTotems[i].pose.x)+(y-self.mapTotems[i].pose.y)*(y-self.mapTotems[i].pose.y)))**0.5
            if(distance<minDist):
                minDist = distance
                idMinDist = i

        return minDist, i

#Class Totem
class Totem:

    def __init__(self):
        
        self.pose = []
        self.totemIdx = 0
        self.IDparent = -1 
        self.listID = [-1,-1,-1,-1] #List ID
        self.listPoseID = [] #List Pose ID

        #***********ID_1***********
        #ID_2******************ID_4
        #***********ID_3***********

    def SetTotemIdx(self, idx):
        self.totemIdx = idx

    def SetID(self, idx, ID):
        self.listID[idx] = ID

    def SetPose(self, pose):
        self.pose = pose

    def SetParent(self, IDparent):
        self.IDparent = IDparent

    def GetParent(self,):
        return self.GetParent

    def TotemFullMapped(self):
        if -1 in self.listID:
            return False
        else:
            return True

    def FilledTotem(self, ID):
        minorID = ID-(2+ID)%4
        for i in range(4):
            self.listID[i] = minorID+i


if __name__ == "__main__":

    #Read Interest Positions
    with open('positions.yaml') as f:
        positionsYaml = yaml.load(f, Loader=yaml.FullLoader)

    numTotems = len(positionsYaml['positions']) #Get number of Intereset Regions
    ourMap = Map(numTotems, positionsYaml)

    #Filled IDs
#    for i in range(ourMap.getSizeMap()):
#        for j in range(4):
#            ourMap.mapTotems[i].SetID(j, 2+4*i+j)
#            #print (ourMap.mapTotems[i].TotemFullMapped())

    vasco = 1000
    