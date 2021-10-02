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


portx = {"001":{"orderIndex": "001", "sside": "Left", "shape":"roundedRect", "image":"None"}}


class BaseModel:

    pass

class BaseObject:

    def __init__(self, name="default"):
        self.objects = {}


class Model:

    def __init__(self, name="default"):
        u = uuid.uuid4()
        self.setRoot(u)
        model = BaseModel()
        self.objects = BaseObject().objects
        self.addObject(name="root", locChildOf=u, typeChildOf=u)

    def setRoot(self, u):
        self.root = u

    def getRoot(self):
        return self.root

    def addObject(self, name="default", ttype="root", location="root", typeChildOf=uuid.uuid4(), locChildOf=uuid.uuid4()):
        u = uuid.uuid4()
        attributes = {}
        groups = {}
        ports = {} #self.getPorts(u)
        self.objects[u] = {"name":name, "type":ttype, "location":location, "typeChildOf":u, "locChildOf":u, "attributes":attributes, "groups":groups, "ports":ports}
        return u

    def instanceObject(self, name="default", ttype="root", location="root", typeChildOf=uuid.uuid4, locChildOf=uuid.uuid4):
        u = uuid.uuid4()
        attributes = self.getAttributes(typeChildOf) #join self.getAttributes(locChildOf)
        groups = {}
        ports = self.getPorts(typeChildOf)
        self.objects[u] = {"name":name, "type":ttype, "location":location, "typeChildOf":typeChildOf, "locChildOf":locChildOf, "attributes":attributes, "groups":groups, "ports":ports}
        return u

    def getPorts(self, u):
        if self.objects[u]['typeChildOf'] == u:
            return self.objects[u]['ports']
        else:
            return self.getPorts(self.objects[u]['typeChildOf'])

    def addAttribute(self, u, att, value):
        self.objects[u].attributes[att] = value

    def getInheritedAttribute(self,u, att):
        if not self.objects[u].attributes(att):
            s = self.getInheritedAttribute(self.objects[self.objects[u].locChildOf], att)
            #here we use recursion to work up the chain of parent objects until the childof object references itself, ultimately 'root' in the furthest case
            while not s == self.objects[self.objects[u].locChhildOf]:
                pass
            return self.objects[self.objects[u].locChildOf]['attributes'[att]]
        return self.objects[u].attributes(att)

    def getAttribute(self, u, att):
        return self.objects[u].attributes(att)

    def getAttributes(self, u):
        return self.objects[u]['attributes']

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

    def multiPort(self, u, port, num= 1, start= 1,):
        oi = 1
        for c in range(start, (start + num)):
            p = {}
            cstr = str(c).zfill(3)
            oistr = str(oi).zfill(3)
            p["orderIndex"] = oistr
            #p['sside'] = port["sside"]
            #p["shape"] = port["shape"]
            #p["image"] = port["image"]
            p["connected"] = 'XYZ'
            self.objects[u]['ports'][cstr] = p
            oi = oi + 1
        return oi

    def listObjects(self):
        for o in self.objects:
            for a in self.objects[o]:
                print(a, self.objects[o][a])
            print()

    def getNameFromuuid(self, u):
        return self.objects[u]['name']

    def getUUIDFromName(self, n):
        # initializing key
        key = "name"
        res1 = []
        for s in self.objects:
            if self.objects[s]['name']==n:
                res1.append(s)
        return res1

    def getFullPathLoc(self,u):
        l=[]
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
    i1 = m.addObject(name="24 Terminals", ttype="Type", typeChildOf=m.getRoot(), location="branch", locChildOf=m.getRoot())


    port = portx
    m.multiPort(i1, port, 24, 1)

    i = m.addObject(name="Kemerton", ttype="Location", typeChildOf=m.getRoot(), location="branch", locChildOf=m.getRoot())
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


    #termMap = ((("Instrument Cable/2.5sqmm", "24 Terminals"), (1,10), (2,11), (3,12),)
    #m.objects.addAttribute("term map", termMap)
    console.log("[red]info [/]", log_locals=True)
    m.listObjects()

    #m.objects(i, addTerminals(terms))

if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

