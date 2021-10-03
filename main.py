from rich.console import Console
from rich.traceback import install
from rich.table import Table
import copy
import uuid

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys


def printf(format, *args):
    sys.stdout.write(format % args)


portx = {"001": {"orderIndex": "001", "sside": "Left", "shape": "roundedRect", "image": "None", 'connections': []}}
standardMap = [("*", "*"), ("001", "001"),("002", "002"),("003", "003"),("004", "004"),("005", "005"),("006", "006"),("007", "007"),("008", "008"),("009", "009"),("010", "010"),("011", "011"),("012", "012"),("013", "013"),("014", "014"),("015", "015"),("016", "016"),("017", "017"),("018", "018"),("019", "019"),("020", "020"),("021", "021"),("022", "022"),("023", "023"),("024", "024"),("025", "025"),("026", "026")]
cable3Pair = {"name": "", "001": "1W", "002": "1B", "003": "1Scn", "004": "2W", "005": "2B", "006": "2Scn", "007": "3W", "008": "3B", "009": "3Scn"}


class BaseModel:
    pass


class BaseObject:

    def __init__(self, name="default"):
        self.objects = {}


class BaseEdge:

    def __init__(self, name="default"):
        self.edges = {}


class Model:

    def __init__(self, name="default"):
        u = uuid.uuid4()
        self.setRoot(u)
        print("root uuid = ", u)
        model = BaseModel()
        self.objects = BaseObject().objects
        self.addObject(name="root", locChildOf=u, typeChildOf=u)
        self.edges = BaseEdge().edges
        self.instanceEdge(name="root")

    def setRoot(self, u):
        self.root = u

    def getRoot(self):
        return self.root

    def instanceEdge(self, name="default", ttype="root", location="root", cores={}, ffrom=uuid.uuid4(), fromPort=portx, to=uuid.uuid4(), toPort=portx):
        u = uuid.uuid4()
        attributes = {}
        groups = {}
        self.edges[u] = {"name": name, "type": ttype, "location": location, "typeChildOf": u, "from": ffrom, "fromPort":fromPort, "to": to, "toPort":toPort,
                         "attributes": attributes, "groups": groups, "cores": cores}
        return u

    def connectEdge(self, edge, cores, fro, fp, fm, too, tp, tm):
        for pt in fp:
            self.objects[fro]['ports'][pt]['connections'].append(self.edges[edge][cores][fm][pt])
#        for pt in tp:
#            self.objects[too]['ports'][pt]['connections'].append(self.edges[edge][cores[tm[pt]]])
        return

    def addObject(self, name="default", ttype="root", location="root", typeChildOf=uuid.uuid4(), locChildOf=uuid.uuid4()):
        u = uuid.uuid4()
        attributes = {}
        groups = {}
        ports = {}  # self.getPorts(u)
        self.objects[u] = {"name": name, "type": ttype, "location": location, "typeChildOf": u, "locChildOf": u,
                           "attributes": attributes, "groups": groups, "ports": ports}
        return u

    def instanceObject(self, name="default", ttype="root", location="root", typeChildOf=uuid.uuid4(),
                       locChildOf=uuid.uuid4()):
        u = uuid.uuid4()
        attributes = self.getAttributes(typeChildOf)  # join self.getAttributes(locChildOf)
        groups = {}
        ports = self.getPorts(typeChildOf)
        self.objects[u] = {"name": name, "type": ttype, "location": location, "typeChildOf": typeChildOf,
                           "locChildOf": locChildOf, "attributes": attributes, "groups": groups, "ports": ports}
        return u

    def getPorts(self, u):
        if u == self.getRoot():
            return[]
        if self.objects[u]['typeChildOf'] == u:
            return self.objects[u]['ports']
        else:
            return self.getPorts(self.objects[u]['typeChildOf'])

    def addAttribute(self, u, att, value):
        self.objects[u].attributes[att] = value

    def getInheritedAttribute(self, u, att):
        if not self.objects[u].attributes(att):
            s = self.getInheritedAttribute(self.objects[self.objects[u].locChildOf], att)
            # here we use recursion to work up the chain of parent objects until the childof object references itself, ultimately 'root' in the furthest case
            while not s == self.objects[self.objects[u].locChhildOf]:
                pass
            return self.objects[self.objects[u].locChildOf]['attributes'[att]]
        return self.objects[u].attributes(att)

    def getAttribute(self, u, att):
        return self.objects[u].attributes(att)

    def getAttributes(self, u):
        if u not in self.objects.keys():
            return []
        if 'attributes' in self.objects[u].keys():
            return self.objects[u]['attributes']
        else:
            return []


    def listAttributes(self):
        l = []
        for k in self.objects.keys():
            l.append(self.objects[k].attributes.keys())
        return l

    def addGroup(self, u, group, value):
        self.objects[u].Groups[group] = value

    def getGroup(self, u, group):
        return self.objects[u].Groups(group)

    def listGroups(self):
        l = []
        for k in self.objects.keys():
            l.append(self.objects[k].Groups.keys())
        return l

    def multiPort(self, u, port, num=1, start=1, ):
        oi = 1
        for c in range(start, (start + num)):
            p = {}
            cstr = str(c).zfill(3)
            oistr = str(oi).zfill(3)
            p["orderIndex"] = oistr
            # p['sside'] = port["sside"]
            # p["shape"] = port["shape"]
            # p["image"] = port["image"]
            p["connected"] = 'XYZ'
            p["connections"] = []
            self.objects[u]['ports'][cstr] = p
            oi = oi + 1
        return oi

    def listObjects(self):
        for o in self.objects:
            for a in self.objects[o]:
                print(a, self.objects[o][a])
            print()

    def listEdges(self):
        for o in self.edges:
            for a in self.edges[o]:
                print(a, self.edges[o][a])
            print()


    def getNameFromuuid(self, u):
        return self.objects[u]['name']

    def getUUIDFromName(self, n):
        # initializing key
        key = "name"
        res1 = []
        for s in self.objects:
            if self.objects[s]['name'] == n:
                res1.append(s)
        return res1

    def getFullPathLoc(self, u):
        l = []
        l.insert(self.objects[u]['name'])


def print_hi(name):
    install()
    # Use a breakpoint in the code line below to debug your script.
    console = Console()
    console.log("[red]info [/]", log_locals=True)
    table = Table()

    byOnes = ["001", "002", "003", "004", "005"]
    m = Model("TestModel")

    i = m.addObject(name="Terminals", ttype="Type", typeChildOf=m.getRoot(), location="branch", locChildOf=m.getRoot())
    i = m.addObject(name="Sac 2.5", ttype="Type", typeChildOf=m.getRoot(), location="branch", locChildOf=m.getRoot())
    i1 = m.addObject(name="24 Terminals", ttype="Type", typeChildOf=m.getRoot(), location="branch",
                     locChildOf=m.getRoot())

    port = portx
    m.multiPort(i1, port, 24, 1)

    i = m.addObject(name="Kemerton", ttype="Location", typeChildOf=m.getRoot(), location="branch",
                    locChildOf=m.getRoot())
    i = m.addObject(name="Train 1", ttype="Location", typeChildOf=m.getRoot(), location="branch", locChildOf=i)
    i = m.addObject(name="2121", ttype="Location", typeChildOf=m.getRoot(), location="branch", locChildOf=i)
    i = m.addObject(name="Switchroom", ttype="Location", typeChildOf=m.getRoot(), location="branch", locChildOf=i)
    i = m.addObject(name="BMS-001", ttype="Location", typeChildOf=m.getRoot(), location="branch", locChildOf=i)
    i = m.addObject(name="Tier 1", ttype="Location", typeChildOf=m.getRoot(), location="branch", locChildOf=i)
    i = m.addObject(name="Pan", ttype="Location", typeChildOf=m.getRoot(), location="branch", locChildOf=i)

    i2 = m.instanceObject(name="2121-BMS001-X01", ttype="Leaf", typeChildOf=i1, location="branch", locChildOf=i)
    m.multiPort(i2, port, 24, 1)
    i2 = m.instanceObject(name="2121-BMS001-X02", ttype="Leaf", typeChildOf=i1, location="branch", locChildOf=i)
    m.multiPort(i2, port, 24, 1)
    i2 = m.instanceObject(name="2121-BMS001-X03", ttype="Leaf", typeChildOf=i1, location="branch", locChildOf=i)
    m.multiPort(i2, port, 24, 1)
    i2 = m.instanceObject(name="2121-BMS001-X04", ttype="Leaf", typeChildOf=i1, location="branch", locChildOf=i)
    m.multiPort(i2, port, 24, 1)

    print("m.getNameFromuuid(ii)", m.getNameFromuuid(i1))
    u = m.getUUIDFromName("Sac 2.5")[0]
    print(u, m.getNameFromuuid(u))

    w = cable3Pair.copy()
    c1 = m.instanceEdge(name="2121-BMS001-X04-J01", ttype="Edge", ffrom=m.getRoot(), fromPort=portx, to=m.getRoot(), toPort=portx,
                          cores=(cable3Pair).copy())
    fr = m.getUUIDFromName("2121-BMS001-X01")[0]
    fp = m.objects[fr]['ports']
    fm = standardMap
    to = m.getUUIDFromName("2121-BMS001-X03")[0]
    tp = m.objects[to]['ports']
    tm = standardMap
    cores = m.edges[c1]['cores']
    c1 = m.connectEdge(c1,cores,fr,fp,fm,to,tp,tm)

    # termMap = ((("Instrument Cable/2.5sqmm", "24 Terminals"), (1,10), (2,11), (3,12),)
    # m.objects.addAttribute("term map", termMap)
    console.log("[red]info [/]", log_locals=True)
    m.listObjects()
    m.listEdges()

    # m.objects(i, addTerminals(terms))


if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
