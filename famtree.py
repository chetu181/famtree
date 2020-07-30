from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

class person:
    def __init__(self,name, gender, yob):
        self.name = name
        self.yob = yob
        self.gender = gender
        self.firstfam = None
        self.secondfam = None
        
    def str(self):
        return self.name+' '+str(self.gender)+' '+str(self.yob)+' '+str(self.firstfam)+' '+str(self.secondfam)

class family:
    def __init__(self, father, mother, childrens):
        self.father = father
        self.mother = mother
        self.childrens = childrens

# #load persons
# chet = person("chaithanya", 1, 3, 4, 1993)
# hars = person("harsha", 2, 3, 4, 1997)
# vid = person("vidya", 3, 5, 6, 1970)
# shank = person("shankarmurthy", 4, 7, 8, 1963)

# persons = [chet, hars, vid, shank]


# pts = []
# for person in persons:
#     print(person.str())
#     pts.append((np.random.random()*10, -person.yob))
#     plt.plot(pts[-1][0], pts[-1][1], 'b.') # TODO: need to ensure siblings come below each other
# # create a graph of persons.

# #TODO: get curved lines
# # TODO: get these info from the graph by an algo
# def connect_pts(pt1, pt2, rel):
#     pt1 -= 1
#     pt2 -= 1
#     plt.plot([pts[pt1][0], pts[pt2][0]], [pts[pt1][1], pts[pt2][1]], 'r-')
# connect_pts(1,2, 's')
# connect_pts(3,1, 'c')
# connect_pts(4,1, 'c')


# plt.show()
np.random.seed(10)

persons = {}
families = []

# load persons from file
famtree_csv_filename = 'famtree.csv'
data = pd.read_csv(famtree_csv_filename)
datalen =  len(data["name"])
print("datalen", datalen)
data = data.replace({np.nan:None})

#add the first person.
i=0
firstper = person(data["name"][i], data["gender"][i], data["yob"][i])
persons[data["name"][i]] = firstper

firstper.firstfam  = family(None, None, [firstper])
firstper.secondfam = family(firstper, None, [])
families.append(firstper.firstfam)
families.append(firstper.secondfam)

# add others in relation to him
for i in range(1,datalen):
    name = data["name"][i]
    gender = data["gender"][i]
    per = person(name, gender, data["yob"][i])
    persons[name] = per
    if(data["sibling_of"][i] is not None):
        sib = persons[data["sibling_of"][i]]
        per.firstfam = sib.firstfam
        per.firstfam.childrens.append(per) #TODO: dont just append, put them in right order
        per.secondfam = family(per if gender=='male' else None , per if gender=='female' else None,[])
        families.append(per.secondfam)

    elif(data["parent_of"][i] is not None):
        child = persons[data["parent_of"][i]]
        per.secondfam = child.firstfam
        if gender == 'male':
            per.secondfam.father = per
        else:
            per.secondfam.mother = per
        per.firstfam = family(None, None, [per])
        families.append(per.firstfam)

    elif(data["spouse_of"][i] is not None):
        spouse = persons[data["spouse_of"][i]]
        per.secondfam = spouse.secondfam
        if gender == 'male':
            per.secondfam.father = per
        else:
            per.secondfam.mother = per
        per.firstfam = family(None, None, [per])
        families.append(per.firstfam)

        
    elif(data["child_of"][i] is not None):
        parent = persons[data["child_of"][i]]
        per.firstfam = parent.secondfam
        per.firstfam.childrens.append(per)
        per.secondfam = family(per if gender=='male' else None , per if gender=='female' else None,[])
        families.append(per.secondfam)

    else:
        pass
        # this must be first person, or someone with no relation before(exception)

# plot families.                                                        
for fam in families:
    xcor = np.random.random()*10
    num_child = len(fam.childrens)
    for child in fam.childrens:
        plt.plot(xcor, -child.yob, 'go' if child.gender=='female' else 'bs')
        child.xcor = xcor
    for i in range(num_child-1):
        plt.plot([xcor]*2 , [ -fam.childrens[i].yob, -fam.childrens[i+1].yob ] , 'r-')

for fam in families:
    num_child = len(fam.childrens)
    if(num_child > 0):
        #find first child and connect.
        if(fam.father is not None):
            plt.plot([fam.father.xcor, fam.childrens[0].xcor], [-fam.father.yob, -fam.childrens[0].yob],'r-')
        if(fam.mother is not None):
            plt.plot([fam.mother.xcor, fam.childrens[0].xcor], [-fam.mother.yob, -fam.childrens[0].yob],'r-')
plt.show()
