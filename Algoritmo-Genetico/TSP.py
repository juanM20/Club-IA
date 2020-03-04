import random
import matplotlib.pyplot as plt
from Cities_Dictionary import cities

def Uniform_random(Population):
    index = random.randint(0, len(Population)-1)
    return index


def Get_Score(Member):

    total_score = 0 
    for i in range(len(Member)-1):
        total_score += cities[Member[i]][Member[i+1]]

    return total_score

def Best_Solution(Population):
    
    best = 10000000

    for Solution in Population:
        if Get_Score(Solution) < best:
            best = Get_Score(Solution)
    
    return [Solution,best]


def Tournament_Select(rounds, Population):

    Champ = -1

    for x in range(0, rounds):
        x=x
        
        contender = Uniform_random(Population)

        if Champ == -1:
            Champ = contender
        elif Get_Score(Population[contender]) < Get_Score(Population[Champ]):
            Champ = contender

    return Population[Champ]

def find_unsed(parent, used):
    
    city_not_used = ''

    for city in parent:
        if city not in used:
            city_not_used = city
            return city_not_used

def slice_crossover_nr(parent1, parent2, cut_length):

    offspring1 = [0 for i in range(0,len(parent1))]
    offspring2 = [0 for i in range(0,len(parent2))]

    used1 = []
    used2 = []

    cutpoint1 = random.randint(0,len(parent1)-cut_length)
    cutpoint2 = cutpoint1 + cut_length

    for i in range(len(parent1)):
        if (i>=cutpoint1) and (i<cutpoint2) :
            offspring1[i] = parent2[i]
            offspring2[i] = parent1[i]
            used1.append(offspring1[i])
            used2.append(offspring2[i])

    for i in range(len(parent1)):
        if (i<cutpoint1) or (i>=cutpoint2) :
            offspring1[i] = find_unsed(parent1,used1)
            used1.append(offspring1[i])
            offspring2[i] = find_unsed(parent2,used2)
            used2.append(offspring2[i])

    return offspring1,offspring2


def Mutation(Mutant):
    
    offspring = Mutant     
    index1 = int(random.randint(0,len(Mutant)-1))
    index2 = -1
    while index2 == -1 or index1 == index2 :
        index2 = int(random.randint(0, len(Mutant)-1)) 
    
    temp = offspring[index1]
    offspring[index1] = offspring[index2]
    offspring[index2] = temp

    return offspring



if __name__ == '__main__':

    ROUNDS = 10
    GENERATIONS = 100
    NUMBER_POPULATION = 500
    PARENTS_PERCENT = 0.5
    MUTATION_PERCENT = 1-PARENTS_PERCENT
    CUT_LENGTH = 5
    
    Champs = []
    Initial_Population = []
    Parents = []
    Mutants = []
    Population = []
    keys = list(cities.keys())
    best_solution = []

    x_axis = []
    y_axis = []
    
    
    # Creamos Población inicial
    for i in range(NUMBER_POPULATION):
        random.shuffle(keys)
        Initial_Population.append(keys.copy())
    
    Population = Initial_Population.copy()
    
    for x in range(GENERATIONS):
        
        Champs.clear()
        # Realizamos una selección por torneo de nuestra población inicial
        for i in range(NUMBER_POPULATION):
            Champ = Tournament_Select(ROUNDS, Population)
            Champs.append(Champ)

        Parents = Champs[:int(len(Champs) * PARENTS_PERCENT )]
        Mutants = Champs[int(len(Champs) * PARENTS_PERCENT):]

        
        Population.clear()
        
        # Realizamos la cruza de los campeones que salieron de la selección
        for i in range(0,len(Parents)-1, 2):
            child1, child2 = slice_crossover_nr(Parents[i],Parents[i+1], CUT_LENGTH)    
            Population.append(child1)
            Population.append(child2)

       
        # Realizamos la mutación        
        for Mutant in Mutants:
            Mutant = Mutation(Mutant)
            Population.append(Mutant)
    
        best_solution = Best_Solution(Population)
        print("Ruta: {}".format(best_solution))


        x_axis.append(x+1)
        y_axis.append(best_solution[1])



    plt.plot(x_axis,y_axis)
    plt.show()
    
    

