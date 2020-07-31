import numpy as np
import pandas as pd
from argparse import ArgumentParser
import plottree

parser = ArgumentParser()
parser.add_argument("--famfile", default='test_dataset.csv',help='name of the file with the family relationship info')
parser.add_argument("--visualise", default='default',help='visualise with respect to who?')
args = parser.parse_args()

class person:
    def __init__(self,name, gender, yob):
        self.name = name
        self.yob = yob
        self.gender = gender
        self.firstfam = None
        self.secondfam = None
        self.xcor = None

    def str(self):
        return self.name+' '+str(self.gender)+' '+str(self.yob)+' '+str(self.firstfam)+' '+str(self.secondfam)

class family:
    def __init__(self, father, mother, childrens):
        self.father = father
        self.mother = mother
        self.childrens = childrens


np.random.seed(40)

persons = {}
families = []

# load persons from file
famtree_csv_filename = args.famfile
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
if(args.visualise=='default'):
    plottree.default(families)
elif(args.visualise not in persons):
    print("ERROR: the person "+args.visualise+" is not in the dataset.")
else:
    key_person = persons[args.visualise]
    plottree.person_centered(key_person, families)
