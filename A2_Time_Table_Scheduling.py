
# coding: utf-8

# In[34]:
################################################
# AI Assignment 2
# Rakesh Rawat MT17046
# Time Table scheduling  using: 
# (1) Genetic Algorithm
# (2) Memetic Algorithm
################################################

import numpy as np
import random
from matplotlib import pyplot as plt
import time


# ## logical constraints
(1) A professor can teach many courses.
(2) Only a single professor can take a single course
(3) At a time, single lecture hall can have a single course only.
(4) All courses should be taught in one week
(5) All professor should be assigned atleast one task in a week
# In[36]:


n_days = 5
n_slots = 8
n_population = 400
mutation_prob = 0.002
memetic_iteration = 50


# In[37]:


# generate data
none = 20
n_pair = 50

p = 20
c = 50   # no of courses
l = 5 #  no. of lecture halls

P = []
C = []


# In[38]:


for i in range(0,p):
    P.append('P'+str(i+1))
for i in range(0,c):
    C.append('C'+str(i+1)) 
    
L = [None for _ in range(0,l)]

P_ = P[:]

for i in range(0,c-p):
    P_.append(random.choice(P))
    #pass

P_C = [(P_[i],C[i]) for i in range(0,len(C))]


# In[39]:


chrom = np.random.choice(a = range(0,n_pair)+[None]*none,size = (n_population,n_days,n_slots,l))
chrom[0]


# In[51]:


def fitness(chrom):
    
    ## gives fitness of a single chromosome
    global n_days,n_slots,l
    penalty = 0
    
    ## slot-wise penalty
    
    for day in chrom:
        for slot in day:
            sched = slot[slot!=None]
            prof = [P_C[i][0] for i in sched]
            course = [P_C[i][1] for i in sched]
            penalty+= len(prof) - len(np.unique(prof))
            penalty+= len(course)-len(np.unique(course))
            
            #print penalty
            
    ## overall
    
    sched = chrom.flatten()
    sched = sched[sched!=None]
    
    overall_prof = [P_C[i][0] for  i in sched]
    overall_course = [P_C[i][1] for i in sched]
    
     
    
    penalty+= n_pair - len(np.unique(overall_prof))
    penalty+= n_pair - len(np.unique(overall_course))
    #print penalty
    return (n_slots*n_days*l)/(penalty*1.0)
    


# In[52]:


def local_search(sol,m):
    
    #choice = [i for i in range(0,n_pair)]
    initial_fitness = fitness(sol)
    max_fitness = initial_fitness
    candidate = sol
    for iters in range(0,m):
        for i,day in enumerate(sol):
            for j,slot in enumerate(day):
                #sched = slot[slot!=None]
                #print slot
                indices = np.setdiff1d(np.arange(len(slot)), np.unique(slot, return_index=True)[1])
                choice = np.setdiff1d(np.arange(n_pair),np.unique(slot))
                for ind in indices:
                    #if slot[ind]!=None:
                        #print "."
                        sol[i][j][ind] = np.random.choice(choice)
        
        fitness_score = fitness(sol)
        
        if iters%5==0 and (max_fitness-initial_fitness)<=0:
            return candidate
        if fitness_score>max_fitness:
            max_fitness = fitness_score
            candidate = np.copy(sol)
    #print (max_fitness-initial_fitness)                    
                
    return candidate
                
                
                


# In[53]:


# for k in range(0,chrom.shape[0]):
#     _,d=local_search(chrom[k],50)
#     print d


# In[54]:


def mutation(chrom):
    global mutation_prob
    
    b = range(0,n_pair)+[None]*(none/4)
    
    random.shuffle(b)
    
    for i,c in enumerate(chrom):
        o = c.flatten()
        k = np.random.uniform(size = o.shape[0])
        indexes = np.where(k<=mutation_prob)
        
        for ind in indexes:
            o[ind] = np.random.choice(b)
        chrom[i] = o.reshape((n_days,n_slots,l))


# In[55]:


def crossover(population):
    
    global chrom,n_days,n_slots,l
    new  = []
    
    np.random.shuffle(population)
    pairs = [population[i*2:(i+1)*2] for i in range(0,len(population)/2)]
    
    for pair in pairs:
        
        p1 = chrom[pair[0]].flatten()
        p2 = chrom[pair[1]].flatten()
        #print np.array_equal(p1.reshape((5,8,10)),chrom[pair[0]])
        x = np.random.randint(low=0,high=len(p1))
        tmp = p1[:x].copy()
        p1[:x] = p2[:x]
        p2[:x] = tmp
        
        new.append(p1.reshape((n_days,n_slots,l)))
        new.append(p2.reshape((n_days,n_slots,l)))
    return np.array(new)   


# In[56]:


def selection(chrom):
    
    fit = {}
    mean_fitness = []
    
    sum_=0.0
    
    for i in range(0,chrom.shape[0]):
        val = fitness(chrom[i])
        mean_fitness.append(val)
        fit[i] = val
        sum_+=val
        
    for key in fit.keys():
        fit[key] = fit[key]/(1.0*sum_)
        
       
    return np.mean(mean_fitness),np.random.choice(fit.keys(),size=(chrom.shape[0],),p = fit.values())


# In[57]:


def memetic(chrom):
    for i,sol in enumerate(chrom):
        chrom[i] = local_search(sol,memetic_iteration)
    return chrom 


# In[58]:


x = []
t = None
prev = None
start_time = time.time()
for iters in range(0,700):

    
    avg,selected = selection(chrom)
    chrom = crossover(selected)
    #mutation(chrom)
    #chrom = memetic(chrom)
    if iters%10==0:
        print "iters :  "+str(iters)+"        Avg Fitness : "+str(avg)
        x.append(avg)
        if prev==avg:
            t =  (time.time()-start_time)
            break
        prev = avg
        
    if iters==400:
        t =  (time.time()-start_time)
    


# In[59]:


def find_best(chrom):
    max_=-99
    sol = None

    for i in chrom:
        f = fitness(i)
        if f>max_:
            max_=f
            sol = i
    print "Max fitness : " + str(max_)
    
    for d,day in enumerate(sol):
        print "DAY : "+str(d+1)+"\n\n"
        for s,slot in enumerate(day):
            print "\tSlot : "+str(s+1)+"\n"
            for c in slot:
                if c!=None:
                    print P_C[c],
                else:
                    print "|XXXX|",
            print "\n"
    
ss = find_best(chrom)
ss


# In[61]:


plt.plot(x)
plt.xlabel('iterations')
plt.ylabel('fitness')
plt.title('MA')
plt.show()


# In[62]:


print "Time : "+str(t)


# ## ======================    CSP ======================

# In[29]:


P_C


# In[63]:


## generate conflict graph

S = {}
G = {}
visited = {}

for f,s in P_C:
    G[s] = []
    visited[s] = 0
    if S.get(f)==None:
        S[f] = [s]
    else:
        S[f].append(s)


## generate conflict graph
for key in S.keys():
    for node1 in S[key]:
        for node2 in S[key]:
            if node1!=node2:
                G[node1].append(node2)
                G[node2].append(node1)
for key in G.keys():
    G[key] = list(set(G[key]))
    
for k in G.keys():
    print k,G[k]


# In[64]:


Available = {}
Size = {}
Assign = {}
ID = {}
ID_assign = {}

for i in range(0,n_days*n_slots):
    ID[i] = l
    ID_assign[i] = []

for f,s in P_C:
    Available[s] = [i for i in range(0,n_days*n_slots)]  # + None
    Assign[s] = []
    Size[s] = len(Available[s])

print Size


# In[65]:


# for _ in range(0,c):
#     new = list(reversed(sorted(Size)))
#     node = new[-1][1]
#     new.remove([new[-1][0],node])
#     Size = new
    
#     if visited[node]==1:
#         continue
#     for id_ in Assign[node]:
#         if ID[id_]!=0:
            
#             for neighbor in G[node]:
#                 if neighbor!=node:
#                     try:
#                         Assign[neighbor].remove(id_)
#                     except:
#                         pass
#             ID_assign[id_].append(node)
#             ID[id_]= ID[id_]- 1
                
                
    
    
            


# In[66]:


count = None

def backtrack(new):
    global count,Size
    
    # pick least constraint node
    if len(new)==0:
        return 
    node = min(new, key=new.get)
    Size[node] = new[node]
    del new[node]
    
    if visited[node]==1:
        pass
    
    for id_color in Available[node]:
        if ID[id_color]!=0:
            
            
            ## delete that color from all the neighbors
            
            for neighbor in G[node]:
                if neighbor!=node:
                    try:
                        
                        Available[neighbor].remove(id_color)
                        new[neighbor]-=1
                    except:
                        pass
            
            ## reduce count from 10 of id
            ID[id_color]-=1
            
            # add that color to node
            Assign[node].append(id_color)
            
            # remove that color from that node
            Available[node].remove(id_color)
            
            ## update the size list
            count = count+1

            if count!=c:
                backtrack(new)
                
        else:
            Available[node].remove(id_color)

                
            
            
            
            
for i in range(0,12):
    global count
    count = 0
    backtrack(Size.copy())

#print Available
print ID

print Assign
print ss

