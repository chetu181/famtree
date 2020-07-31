import numpy as np
from matplotlib import pyplot as plt

def plot_person(person, ax):
    ax.plot(person.xcor, -person.yob, 'go' if person.gender=='female' else 'bs')
    ax.text(person.xcor, -person.yob,person.name)

def connect_people(pt1, pt2, rel, style, ax):
    if(pt1.xcor is not None and pt1.xcor is not None):
        ax.plot([pt1.xcor, pt2.xcor], [-pt1.yob, -pt2.yob], style)


def default(families):
    print("default plot")
    fig, ax = plt.subplots(figsize=(16,9))
    for fam in families:
        xcor = np.random.random()*10
        num_child = len(fam.childrens)
        for child in fam.childrens:
            child.xcor = xcor
            plot_person(child, ax)

        for i in range(num_child-1):
            ax.plot([xcor]*2 , [ -fam.childrens[i].yob, -fam.childrens[i+1].yob ] , 'r-')

    for fam in families:
        num_child = len(fam.childrens)
        if(num_child > 0):
            #find first child and connect.
            if(fam.father is not None):
                connect_people(fam.father, fam.childrens[0], 'c', 'r-', ax)
            if(fam.mother is not None):
                connect_people(fam.mother, fam.childrens[0], 'c', 'r--', ax)
    plt.show()

def plot_descendents(family, minx, maxx, ax):
    '''plots everyone with random xcor in minmaxx range'''
    famxcor = minx + np.random.random()*(maxx-minx)
    for child in family.childrens:
        child.xcor = famxcor
        plot_person(child, ax)
        plot_descendents(child.secondfam, minx, maxx, ax)

def person_centered(key_person, families):
    print("drawing tree with respect to "+key_person.name)
    fig, ax = plt.subplots(figsize=(16,9))

    #plot person
    key_person.xcor = 0
    plot_person(key_person, ax)

    #plot ancestors and cousins
    def expand_one_side(queue, sign):
        diff = sign
        val = sign
        head = 0
        while(head<len(queue)): #bfs
            foref = queue[head]
            head +=1
            if(foref is None):
                continue
            #plot forefather
            foref.xcor = val
            plot_person(foref, ax)
            
            queue.append(foref.firstfam.mother)
            queue.append(foref.firstfam.father)

            #plot forefathers descendents
            for child in foref.firstfam.childrens:
                if child is not foref:
                    child.xcor = foref.xcor
                    plot_person(child, ax)
                    plot_descendents(child.secondfam, val , val+diff, ax)
            val += diff
    expand_one_side([key_person.firstfam.father], -10)
    expand_one_side([key_person.firstfam.mother], 10)
    # plot siblings and descendents
    for child in key_person.firstfam.childrens:
        child.xcor = 0
        plot_person(child, ax)
        plot_descendents(child.secondfam, -10, 10, ax)

    #connect 
    for fam in families:
        num_child = len(fam.childrens)
        #connect parents
        if(num_child > 0):
            #find first child and connect.
            if(fam.father is not None):
                connect_people(fam.father, fam.childrens[0], 'c', 'r--', ax)
            if(fam.mother is not None):
                connect_people(fam.mother, fam.childrens[0], 'c', 'r-', ax)
        #connect siblings
        num_child = len(fam.childrens)
        for i in range(num_child-1):
            connect_people(fam.childrens[i], fam.childrens[i+1], 's', 'g-', ax)
    plt.show()
    pass