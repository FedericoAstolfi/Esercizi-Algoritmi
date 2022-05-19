
import sys
import random
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from numpy import NaN
import math
import copy
'''la mia idea è di creare una città 0 da cui si parte sempre di base + ncities-1 città, sui cui fare una
permutazione di 1...ncities-1. Quindi un totale di ncities città da percorrere.
Inoltre come funzione di fitness useremo l'inverso del quadrato della distanza totale percorsa, ma all'
interno della classe City definiamo un metodo che calcola la distanza (regolare) tra la città stessa e un'altra'''

def distance(x1,x2,y1,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

class City():
    '''le città vengono labelled con un intero da 0 a ncities-1 e hanno coordinate random in IxI, la città
    numero 0 verrà messa nell'origine '''
    def __init__(self, int=0):
        if not int==0:
            self.x=random.random()
            self.y=random.random()
        else:
            self.x=0
            self.y=0
    def get_distance(self,other):
        return distance(self.x,other.x,self.y,other.y)
        

class Viaggiatore:
    def __init__(self,list):
        self.cammino=[0]
        self.cammino+=list
        self.cammino+=[0]
    def get_fitness(self, list):
        distance_squared=0
        for i in range(0,ncities-1):
            distance_squared+=list[self.cammino[i]].get_distance(list[self.cammino[i+1]])
        '''il pezzo che segue non l'ho inserito direttamente nel cicl perchè in prima battuta
        non avevo incluso lo 0 anche alla fine del cammino, ma in tal modo nel plot non si vede
        che il venditore torna indietro. quindi a posteriori ho aggiunto lo 0 anche alla fine ma era
        tardi e non volevo fare cavolate con gli indici e scombinare qualcosa, tanto più che dovrebbe
        funzionare comunque correttamente'''
        distance_squared+=list[self.cammino[ncities-1]].get_distance(list[self.cammino[0]])
        distance=math.sqrt(distance_squared)
        return 1/distance
    def mate(self,other, posizioni=[]):
        list1=self.cammino[1:ncities]
        list2=other.cammino[1:ncities]
        return Viaggiatore(crossover(list1,list2, positions=posizioni))
    def mutate(self):
        pass
    

def generate_population(npop):
    '''genera una lista di viaggiatori'''
    population=[]
    for i in range(npop):
        population+=[Viaggiatore(random.sample(range(1, ncities),ncities-1))]
    return population


       
def crossover(list1, list2, n=4, positions=[]):  
    '''order based crossover'''
    assert(len(list1)==len(list2))

    result=[-1 for i in range(len(list1))]
    if not positions:
        positions=random.sample((range(len(list1))),n)
        positions.sort()
    #print(positions)
    elements1=[list1[i] for i in positions]
    #print(elements1)
    
    counter=0
    for i in range(len(list1)):
        
        if not list2[i] in elements1:
            result[i]=list2[i]
            
        else:
            result[i]=elements1[counter]
            counter+=1
    return result

def roulette_sampling(list,fit):
    '''associamo virtualmente all'elemento i-esimo della list la probabilità i-esima di prob'''
    assert(len(list)==len(prob))
    prob=copy.copy(fit)
    prob=prob/np.sum(prob)
    cum=np.cumsum(prob)
    cum=cum.tolist()
    rn=random.random()
    for i in cum:
        if rn<i:
            return list[cum.index(i)]



if __name__=='__main__':

    parser = argparse.ArgumentParser(description = "A program running genetic algorithms")
    parser.add_argument('ncities', help='number of cities', type=int)
    parser.add_argument('popsize', help= "Population size", type=int)
    parser.add_argument('surv_frac', help= "Surviving fraction", type=float)
    parser.add_argument('mut_prob', help= "Mutation probability", type=float)
    parser.add_argument('ngen', help= "N of generations", type=int)
    parser.add_argument('--no_plots', help="does not show plots", default=False, action='store_true')
    args = parser.parse_args()

    print(args)

    npop = args.popsize
    surv_prob = args.surv_frac
    mut_prob = args.mut_prob
    ngen = args.ngen
    ncities = args.ncities

    '''dopo questa prima parte tecnica, cominciamo dal creare le nostre città'''
    cities=[]
    for i in range(ncities):
        cities+=[City(i)]

    '''creaimo una popolazione'''
    pop=generate_population(npop)
    
    '''otteniamo il best score e il worst score per questa prima popolazione'''
    best_score=max([viag.get_fitness(cities) for viag in pop ])
    print(best_score)
    worst_score=min([viag.get_fitness(cities) for viag in pop ])
    print(worst_score)
    '''qua faccio uno prova per la prima generazione e stampo il più veloce e  il più lento'''
    top_viag=NaN
    worst_viagg=NaN
    for viag in pop:
        if best_score==viag.get_fitness(cities):
            top_viag=viag
    for viag in pop:
        if worst_score==viag.get_fitness(cities):
            worst_viag=viag


    fig, ax = plt.subplots(1,3, figsize=(10,5))
    #plot of the cities
    ax[0].set_xlim(-0.1,1)
    ax[0].set_ylim(-0.1,1)
    ax[0].scatter([city.x for city in cities],[city.y for city in cities])
    ax[0].scatter(0,0)
    ax[0].plot([cities[i].x for i in top_viag.cammino],[cities[i].y for i in top_viag.cammino],'g')
    ax[0].plot([cities[i].x for i in worst_viag.cammino],[cities[i].y for i in worst_viag.cammino],'r')


    #print(pop[0].cammino)
    #print(pop[1].cammino)
    #print(pop[0].mate(pop[1], [1,3,5,7]).cammino)





    plt.show()


    