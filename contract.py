from location import locs as locations
from location import coords as stations
from cargo import types
from cargo import compT
from cargo import sizes

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


def doRoute(route:list[str], vesselSize:int, contracts:list[Contract], verbose:bool=True)->None:
    """
    Executes the route, giving position info and warnings for overcapacity.
    If verbose is set to True (default), also gives loading and unloading instructions as well as capacity info.
    """
    hold = {}
    holdSCU = 0
    for step in route:
        if not(validLoc(step)):
            print("{0} is not a valid location.".format(step))
            return None
    print("Route starting point: {}".format(route[0]))
    for step in route:
        if step != route[0]:
            print("Loaded, departing for {}.".format(step))
            print("\n")
            print("Arriving at {}".format(step))
        # unload
        if holdSCU == 0:
            pass
        else:
            print(hold)
            if step in hold:
                text = ''
                for cargo in hold[step]:
                    amount = cargo[0]
                    type = cargo[1]
                    if verbose: 
                        if text == '':
                            text = "Unloading cargo :"
                        if text[-1] != ':':
                            text += ","
                        text += " {0} {1}".format(amount, type)
                    holdSCU -= amount
                hold.pop(step)
                if verbose:
                    print(text)
        # load
        load = {}
        for c in contracts:
            for srcType in c.content:
                if step == srcType[0]:
                    for dest in c.content[srcType][1]:
                        if dest in load:
                            load[dest].append((c.content[srcType][1][dest], srcType[1]))
                        else:
                            load[dest] = []
                            load[dest].append((c.content[srcType][1][dest], srcType[1]))
        for dest in load:
            text = ''
            if verbose:
                text = "Loading cargo to {0}:".format(dest)
                for cargo in load[dest]:
                    amount = cargo[0]
                    type = cargo[1]
                    if text[-1] != ':':
                        text += ","
                    text += " {0} {1}".format(amount, type)
                print(text)
            if not(dest in hold):
                hold[dest] = []
            hold[dest] += load[dest]
            for l in load[dest]:
                holdSCU += l[0]
        load = {} #debug vizualisation
        if holdSCU > vesselSize:
            sss = 's'
            if holdSCU-vesselSize == 1:
                sss = ''
            print("Overcapacity by {0} SCU{1}.".format(holdSCU-vesselSize, sss))
        elif verbose:
            print("Carrying {}/{} SCUs ({}%).".format(holdSCU, vesselSize, int(100*holdSCU/vesselSize)))
    print("Route finished. Currently located at {}.".format(route[-1]))
    if route[0] == route[-1]:
        print("This was also the starting point. Welcome back!")
    if holdSCU != 0:
        sss = 's'
        if holdSCU == 1:
            sss = ''
        print("You still have {0} SCU{1} undelivered!!!".format(holdSCU, sss))


contracts = []

contracts.append(Contract())
#print(c1)
contracts[0].addSource("Seraphim Station", "Hydrogen")
#print(c1)
contracts[0].addDest("Seraphim Station", "Everus Harbor", 102, "Hydrogen")
contracts[0].addDest("Seraphim Station", "Baijini Point", 92, "Hydrogen")
contracts.append(Contract())
contracts[1].addDest("Everus Harbor", "HUR-L5", 96, "Quantum Fuel")
contracts[1].addDest("HUR-L5", "Everus Harbor", 139, "Hydrogen Fuel")
contracts[1].addDest("Everus Harbor", "HUR-L5", 142, "Ship Ammunition")
print("\n")
for c in contracts:
    print(c)

print("\n\n")
print("Routing test")
print("\n\n")
route = ["Seraphim Station", "Everus Harbor", "HUR-L5", "Baijini Point"]
doRoute(route, 696, contracts, True)
