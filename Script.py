
import itertools

# Net class: Contains the name of the net and the faults that are associated with it
class Net:
    all = []  # List of all instances
    all_instances_names = []
    def __init__(self,name):
        self.name = name
        self.faults = ["sa0","sa1"]  # Default faults: Fault Population
        Net.all.append(self)         
        Net.all_instances_names.append(name)
        
    def __repr__(self):
        return f"Net_{self.name}" 
    

# EquivalentFaultCollapsing function: This function takes each gate with netlist as collapses the equivalent faults    

def EquivalentFaultCollpasing(property):

    if property[0] in ["FANOUT","INPUT","OUTPUT"] :
        # No Equivalence possible in inputs, Fanout Nodes
        return 

    elif property[0] in ["AND","NAND"]:
        # For AND and NAND gates, Input sa0 fault are equivalent to sa0 and sa1 faults
        # at output respectively. So,input sa0 can be eliminated.

        for inp in property[2:]:
            for net in Net.all:
                if net.name == inp:
                    if "sa0" in net.faults:
                        net.faults.remove("sa0")
        return
    elif property[0] in ["OR","NOR"]:
        # For OR and NOR gates, Input sa1 fault are equivalent to sa1 and sa0 faults
        # at output respectively. So,input sa1 can be eliminated.
        for inp in property[2:]:
            for net in Net.all:
                if net.name == inp:
                    if "sa1" in net.faults:
                        net.faults.remove("sa1")
        return
    elif property[0] == "NOT":
        # For NOT gate, Input sa0,sa1 fault are equivalent to sa1,sa0 repectively fault at output.
        # So,input sa0 and sa1 can be eliminated.
        for net in Net.all:
            if net.name == property[2]:
                if "sa0" in net.faults:
                    net.faults.remove("sa0")
                if "sa1" in net.faults:
                    net.faults.remove("sa1")
        return




# FaultPopulation function: This function populates the faults for each node in the netlist

def faultPopulation(file):

    nodelist = []
    for prop in file:
        nodelist.append(prop[1:])

    nodelist =  list(set(itertools.chain(*nodelist)))

    # Populating the faults for each node 
    for node in nodelist:
        Net(node)
    
    total_faults = 2*len(nodelist)

    return total_faults



def main():

    with open("netlist.txt") as f:
        netlist = f.readlines()

    # Cleaning the netlist
    for i in range(len(netlist)):
        netlist[i] = netlist[i].split()
        netlist[i] = [x for x in netlist[i] if x != '']

    TotalFaultBeforeCollapsing = faultPopulation(netlist)
    print("\nPopulated Fault list for each node :")

    for net in Net.all:
        print(f"Net : {net.name}, Faults: {net.faults}")

    print(f"\nTotal Faults before Collapsing :{TotalFaultBeforeCollapsing}")

    print("------------------------------------")
    # Fault collapsing
    for prop in netlist:
        EquivalentFaultCollpasing(prop)
        # This function will remove the equivalent faults from the fault list of the nodes

    print("Fault list after Equivalence Fault Collapsing :\n")

    NumFaultsAfterCollapsing = 0

    for net in Net.all:

        print(f"Net :{net.name},  Faults: {net.faults}")
        NumFaultsAfterCollapsing += len(net.faults)

    print("------------------------------------")   

    print(f"Collapse Ratio :{NumFaultsAfterCollapsing}/{TotalFaultBeforeCollapsing}")

    print("------------------------------------")

if __name__ == "__main__":
    main()


    