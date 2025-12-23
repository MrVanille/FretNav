import math

class StellarObject():
    def __init__(self, name:str, system:str, azimuth:float, polar:float, dist:float, type:str="Other")->None:
        if not(type in ["Star", "Planet", "Gateway", "Station", "Other"]):
            type = "Other"
        self.name = name
        self.system = system
        self.type = type
        self.azimtuh = azimuth
        self.polar = polar
        self.dist = dist
        self.coords = (dist, polar, azimuth)
    
    def isGate(self)->bool:
        if self.type == "Gateway":
            return True
        return False
    def isPlanet(self)->bool:
        if self.type == "Planet":
            return True
        return False
    
    def distanceTo(self, dest:tuple[float])->float:
        """
        Calculates distance (in Gigameters) between the object and the coordinates in dest using spherical coords (dist, polar, azimuth).
        """
        # assert loc1[1] == loc2[1]     # same system
        d = math.sqrt(self.coords[0]**2 + dest[0]**2 - 2*self.coords[0]*dest[0]*(math.sin(self.coords[1]*math.pi/180)*math.sin(dest[1]*math.pi/180)*math.cos((dest[2]-self.coords[2])*math.pi/180) + math.cos(self.coords[1]*math.pi/180)*math.cos(dest[1]*math.pi/180)))
        return d


# instanciate all from location.locs