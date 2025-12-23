from location import locs as locations
from location import coords as stations
from cargo import types
from cargo import compT
from cargo import sizes
from location import distanceCalc

def validLoc(loc:str)->(bool | str):
    """
    Check if location is referenced.
    This will be useful for future features, like routing, which require coordinates.
    Returns False if the location isn't in the database, and a correctly formatted version if it is
    """
    for l in locations:
        if l.lower() == loc.lower():
            return l
    for s in stations:
        if s.lower() == loc.lower():
            return s
    return False


class Contract():
    def __init__(self):
        self.content = {}

    def addSource(self, src:str, type:str)->None:
        """
        Adds a source to the contract
        """
        src = validLoc(src)
        if src == False:
            print("Unknown source, this only supports Lagrange point stations and planets' surfaces, orbital stations, main city and spaceport")
        else:
            self.content[(src, type)] = [0, {}]

    def addDest(self, src:str, dest:str, amount:int, type:str)->None:
        """
        Adds a destination to the selected source
        """
        srcNotPresent = True
        if type == '': # necessary to prevent empty key for dict search, add valid type on top
                print("This source does not exist in this contract yet, add it first or give a valid cargo type.")
        else:
            for s in self.content:
                if s == (src, type):
                    srcNotPresent = False
                    break
            if srcNotPresent:
                print("This source does not exist in this contract yet, trying to add it...")
                self.addSource(src, type)
                self.addDest(src, dest, amount, type)
            else:
                dest = validLoc(dest)
                if dest == False:
                    print("Unknown source, this only supports Lagrange point stations and planets' surfaces, orbital stations, main city and spaceport")
                else:
                    self.content[(src, type)][1][dest] = amount
                    self.content[(src, type)][0] += amount

    def delSource(self, src:str, type:str)->None:
        """
        Deletes the source from the contract
        """
        if (src, type) in self.content:
            self.content.pop((src, type))
            print("Successfully deleted source!")
        else:
            print("This source does not exist, cannot remove it!")

    def delDest(self, src:str, dest:str, type:str, delEmptySource=False)->None:
        """
        Deletes the destination from selected source, as well as the source if it is now empty and delEmptySource is set to True 
        """
        if dest in self.content[(src, type)][1]:
            self.content[(src, type)][1].pop(dest)
            print("Successfully deleted destination!")
            if self.content[(src, type)][1] == {} and delEmptySource:
                print("Deleting empty source...")
                self.delSource(self, src, type)
        else:
            print("This destination does not exist for this source!")

    def __str__(self):
        """
        Return contract in a string matching the mobiGlas' Contracts Manager screen's formatting
        """
        if self.content == {}:
            return "This contract is empty!"
        text = ""
        for src in self.content:
            text += "Collect {0} {1} from {2}.\n".format(self.content[src][0], src[1], src[0])
            if self.content[src][1] == {}:
                text += "   This source has no destinations!\n"
            else:
                for dest in self.content[src][1]:
                    text += "   Deliver {0} {1} to {2}.\n".format(self.content[src][1][dest], src[1], dest)
        return text