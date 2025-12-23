from contract import Contract
from contract import validLoc
from location import locs as locations
from location import coords as stations
from cargo import types
from cargo import compT
from cargo import sizes
from location import distanceCalc

def doRoute(route:list[str], vesselSize:int, contracts:list[Contract], verbose:bool=True)->None:
    """
    Executes the route, giving position info and warnings for overcapacity.
    If verbose is set to True (default), also gives loading and unloading instructions as well as capacity info and distance calculation before routing.
    """
    
    # Route validation
    stepsAdded = 0
    route[0] = validLoc(route[0])
    if validLoc(route[0]) == False:
        print("{0} is not a valid location.".format(route[0]))
        return None
    for i in range(len(route)):
        step = i + stepsAdded   # Shift the cursor when locations are added by this loop
        if step != len(route)-1:
            route[step+1] = validLoc(route[step+1])
            if validLoc(route[step+1]) == False:
                print("{0} is not a valid location.".format(route[step+1]))
                return None
            if route[step] in locations:
                loc1 = stations[locations[route[step]]]
            else:
                loc1 = stations[route[step]]
            if route[step+1] in locations:
                loc2 = stations[locations[route[step+1]]]
            else:
                loc2 = stations[route[step+1]]
            if (loc1[1][-7:] == "Gateway" and loc2[1][-7:] == "Gateway") and (loc1[1][:-7] == loc2[1] and (loc2[1][:-7] == loc1[1])):
                route.pop(step+1)   # Gateway going its twin in the other system
                stepsAdded -= 1
            elif (loc1[1][-7:] == "Gateway" and loc1[1][:-7] == loc2[1]) or (loc1[1] == loc2[1]):
                pass    # (Gateway going to the next step's system AND not its twin) OR both in same system
            elif loc1[1] != loc2[1] and (loc1[1][-7:] != "Gateway"):
                if "{0} Gateway".format(loc2[1]) in stations and stations["{0} Gateway".format(loc2[1])] == loc1[1]:
                    print("These two stations are in neighbour systems, adding the gateway between them.")
                    #if gate exists
                    route.insert("{0} Gateway".format(stations[loc2][1]))
                    stepsAdded += 1
                else:
                    print("Gateway validation issue (elif): {0} -> {1}".format(loc1, loc2))
            else:
                print("Gateway validation issue (else): {0} -> {1}".format(loc1, loc2))
    if len(route) in [0, 1]:
        print("A route needs at least a starting point and a destination!")
        return None
    maxlen = 0
    for step in route:
        if len(step) > maxlen:
            maxlen = len(step)
    
    # Route printing
    print("Route:\n")
    for i in range(len(route)):
        if i == 0:
            print("Starting point ->     {}".format(route[i].center(maxlen)))
            print("                      {}".format("↓".center(maxlen)))
        elif i == len(route)-1:
            print("                      {}  <- Destination".format(route[i].center(maxlen)))
        else:
            print("                      {}".format(route[i].center(maxlen)))
            print("                      {}".format("↓".center(maxlen)))
    print("\n")
    
    # Distance info
    distanceTraveled = 0
    for i in range(len(route)-1):
        distanceStep = distanceCalc(route[i], route[i+1])
        if verbose:
            print("Distance from {0} to {1}: {2}.{3}Gm".format(route[i], route[i+1], int(distanceStep), int((distanceStep*100)%100)))
        distanceTraveled += distanceStep
    if verbose:
        print("In total, you should travel around {0}.{1}Gm during this route.".format(int(distanceTraveled), int((distanceTraveled*100)%100)))
        print("\n")
    
    # Route execution
    hold = {}
    holdSCU = 0
    for step in route:
        if step != route[0]:
            print("Loaded, departing for {}.".format(step))
            print("\n")
            print("Arriving at {}".format(step))
        # unload
        if holdSCU == 0:
            pass
        else:
            #print(hold) #show content of the hold upon arriving (DEBUG)
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
        if holdSCU > vesselSize:
            sss = 's'
            if holdSCU-vesselSize == 1:
                sss = ''
            print("Overcapacity by {0} SCU{1}.".format(holdSCU-vesselSize, sss))
        elif verbose:
            print("Carrying {}/{} SCUs ({}%).".format(holdSCU, vesselSize, int(100*holdSCU/vesselSize)))

    # Route finished
    print("Route finished. Currently located at {}.".format(route[-1]))
    if route[0] == route[-1]:
        print("This was also the starting point. Welcome back!")
    print("\nYou have travelled around {0}.{1}Gm during this route.".format(int(distanceTraveled), int((distanceTraveled*100)%100)))
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
print("Active Contracts:\n")
for c in contracts:
    print(c)

print("\n\n")
print("Routing test")
print("\n\n")
route = ["Seraphim Station", "Everus Harbor", "HUR-L5", "Baijini Point"]
doRoute(route, 696, contracts, False)
