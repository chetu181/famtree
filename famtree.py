from matplotlib import pyplot as plt
import numpy as np

class person:
    def __init__(self,name, id, mother_id, father_id, yob):
        self.name = name
        self.id = id
        self.mother_id = mother_id
        self.father_id = father_id
        self.yob = yob
    
    def str(self):
        return self.name+' '+str(self.id)+' '+str(self.mother_id)+' '+str(self.father_id)+' '+str(self.yob)+' '

#load persons
chet = person("chaithanya", 1, 3, 4, 1993)
hars = person("harsha", 2, 3, 4, 1997)
vid = person("vidya", 3, 5, 6, 1970)
shank = person("shankarmurthy", 4, 7, 8, 1963)

persons = [chet, hars, vid, shank]

pts = []
for person in persons:
    print(person.str())
    pts.append((np.random.random()*10, -person.yob))
    plt.plot(pts[-1][0], pts[-1][1], 'b.') # TODO: need to ensure siblings come below each other
# create a graph of persons.

#TODO: get curved lines
# TODO: get these info from the graph by an algo
def connect_pts(pt1, pt2, rel):
    pt1 -= 1
    pt2 -= 1
    plt.plot([pts[pt1][0], pts[pt2][0]], [pts[pt1][1], pts[pt2][1]], 'r-')
connect_pts(1,2, 's')
connect_pts(3,1, 'c')
connect_pts(4,1, 'c')

xs = [1,2,3,4] 
ys = [2,4,1,6]
# plt.plot(xs, ys)
plt.show()