import math

locs = {
    "Everus Harbor":            "HUR",
    "Teasa Spaceport":          "HUR",
    "Lorville":                 "HUR",
    "Hurston":                  "HUR",
    "Seraphim Station":         "CRU",
    "August Dunlow Spaceport":  "CRU",
    "Orison":                   "CRU",
    "Crusader":                 "CRU",
    "Baijini Point":            "ARC",
    "Riker Memorial Spaceport": "ARC",
    "Area 18":                  "ARC",
    "Arccorp":                  "ARC",
    "Port Tressler":            "MIC",
    "New Babbage":              "MIC",
    "microTech":                "MIC"
} # Location                    Object

coords = {
    "HUR":              ((12.85, 0, 0), "Stanton"),
    "HUR-L1":           ((11.56, 0, 0), "Stanton"),
    "HUR-L2":           ((14.13, 0, 0), "Stanton"),
    "HUR-L3":           ((12.84, 180, 0), "Stanton"),
    "HUR-L4":           ((12.84, 60, 0), "Stanton"),
    "HUR-L5":           ((12.85, -60, 0), "Stanton"),
                
    "CRU":              ((19.14, -172, 0), "Stanton"),
    "CRU-L1":           ((17.23, -172, 0), "Stanton"),
    "CRU-L2":           ((21.06, -172, 0), "Stanton"),
    "CRU-L3":           ((19.14, 8, 0), "Stanton"),
    "CRU-L4":           ((19.14, -112, 0), "Stanton"),
    "CRU-L5":           ((19.14, 128, 0), "Stanton"),
                
    "ARC":              ((28.91, -50, 0), "Stanton"),
    "ARC-L1":           ((26.02, -50, 0), "Stanton"),
    "ARC-L2":           ((31.81, -50, 0), "Stanton"),
    "ARC-L3":           ((28.92, 150, 0), "Stanton"),
    "ARC-L4":           ((28.91, 10, 0), "Stanton"),
    "ARC-L5":           ((28.92, -110, 0), "Stanton"),
                
    "MIC":              ((43.44, 58.9, 0), "Stanton"),
    "MIC-L1":           ((39.09, 58.9, 0), "Stanton"),
    "MIC-L2":           ((47.79, 58.9, 0), "Stanton"),
    "MIC-L3":           ((43.43, -121.1, 0), "Stanton"),
    "MIC-L4":           ((43.45, 118.9, 0), "Stanton"),
    "MIC-L5":           ((43.45, -1.1, 0), "Stanton"),

    "Pyro Gateway":     ((28.3, -83.25, -5.42), "Stanton"),
    "Stanton Gateway":  ((53.06, 50, 0), "Pyro")

    
} # Planet/Station      Distance to star in Gm, Angle in degrees, Deviation from system's elliptic plane in degrees
  # In Star Citizen's map, this is shown in the reverse way     ->     Deviation, Angle, Distance


def distanceCalc(loc1name:str, loc2name:str)->float:
    """
    Calculates distance (in Gigameters) between two locations using their spherical coordinates
    """
    if loc1name in locs:
        loc1name = locs[loc1name]
    if loc2name in locs:
        loc2name = locs[loc2name]
    loc1, loc2 = coords[loc1name], coords[loc2name]
    assert loc1[1] == loc2[1]
    d = math.sqrt(loc1[0][0]**2 + loc2[0][0]**2 - 2*loc1[0][0]*loc2[0][0]*(math.sin(loc1[0][1]*math.pi/180)*math.sin(loc2[0][1]*math.pi/180)*math.cos((-loc1[0][2]+loc2[0][2])*math.pi/180) + math.cos(loc1[0][1]*math.pi/180)*math.cos(loc2[0][1]*math.pi/180)))
    return d

'''
class Location():
    def __init__(self, name, coord, system):
        self.loc = name
        self.coord = coord
        self.system = system'''
#print(distanceCalc("HUR", "Arccorp"))