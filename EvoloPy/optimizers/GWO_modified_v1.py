# -*- coding: utf-8 -*-
"""
Created on Mon May 16 00:27:50 2016

@author: Hossam Faris
"""

import random
import numpy
import math
from EvoloPy.solution import solution
import time


def distance_to_optimum(centroid,k):

    optimum = numpy.full_like(centroid, k)  
    distance = numpy.linalg.norm(centroid - optimum)  

    return distance

def GWO_modified_v1(objf, lb, ub, dim, SearchAgents_no, Max_iter):

    # Max_iter=1000
    # lb=-100
    # ub=100
    # dim=30
    # SearchAgents_no=5

    # initialize alpha, beta, and delta_pos
    Alpha_pos = numpy.zeros(dim)
    Alpha_score = float("inf")

    Beta_pos = numpy.zeros(dim)
    Beta_score = float("inf")

    Delta_pos = numpy.zeros(dim)
    Delta_score = float("inf")

    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim

    # Initialize the positions of search agents
    Positions = numpy.zeros((SearchAgents_no, dim))
    for i in range(dim):
        Positions[:, i] = (
            numpy.random.uniform(0, 1, SearchAgents_no) * (ub[i] - lb[i]) + lb[i]
        )

    Convergence_curve = numpy.zeros(Max_iter)
    s = solution()

    # Loop counter
    print('GWO_modified_v1 is optimizing  "' + objf.__name__ + '"')

    s.centroid_all = []
    s.centroid_leaders = []
    s.centroid_all_distance = []
    s.centroid_leaders_distance = []
    # s.movement_vectors = []

    timerStart = time.time()
    s.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    # Main loop
    for l in range(0, Max_iter):
        for i in range(0, SearchAgents_no):

            for j in range(dim):
                Positions[i, j] = numpy.clip(Positions[i, j], lb[j], ub[j])

            # Calculate objective function for each search agent
            fitness = objf(Positions[i, :])

            # Update Alpha, Beta, and Delta
            if fitness < Alpha_score:
                Delta_score = Beta_score  # Update delte
                Delta_pos = Beta_pos.copy()
                Beta_score = Alpha_score  # Update beta
                Beta_pos = Alpha_pos.copy()
                Alpha_score = fitness
                # Update alpha
                Alpha_pos = Positions[i, :].copy()
                alpha_index = i

            if fitness > Alpha_score and fitness < Beta_score:
                Delta_score = Beta_score  # Update delte
                Delta_pos = Beta_pos.copy()
                Beta_score = fitness  # Update beta
                Beta_pos = Positions[i, :].copy()
                beta_index = i

            if fitness > Alpha_score and fitness > Beta_score and fitness < Delta_score:
                Delta_score = fitness  # Update delta
                Delta_pos = Positions[i, :].copy()
                delta_index = i


        a = 2 - l * ((2) / Max_iter)
        # a decreases linearly fron 2 to 0

        # Update the Position of search agents including omegas
        for i in range(0, SearchAgents_no):
            for j in range(0, dim):

                r1 = random.random()  # r1 is a random number in [0,1]
                r2 = random.random()  # r2 is a random number in [0,1]

                A1 = 2 * a * r1 - a
                # Equation (3.3)
                C1 = 2 * r2
                # Equation (3.4)

                D_alpha = abs(C1 * Alpha_pos[j] - Positions[i, j])
                # Equation (3.5)-part 1
                X1 = Alpha_pos[j] - A1 * D_alpha
                # Equation (3.6)-part 1

                r1 = random.random()
                r2 = random.random()

                A2 = 2 * a * r1 - a
                # Equation (3.3)
                C2 = 2 * r2
                # Equation (3.4)

                D_beta = abs(C2 * Beta_pos[j] - Positions[i, j])
                # Equation (3.5)-part 2
                X2 = Beta_pos[j] - A2 * D_beta
                # Equation (3.6)-part 2

                r1 = random.random()
                r2 = random.random()

                A3 = 2 * a * r1 - a
                # Equation (3.3)
                C3 = 2 * r2
                # Equation (3.4)

                D_delta = abs(C3 * Delta_pos[j] - Positions[i, j])
                # Equation (3.5)-part 3
                X3 = Delta_pos[j] - A3 * D_delta
                # Equation (3.5)-part 3

                Positions[i, j] = (X1 + X2 + X3) / 3  # Equation (3.7)

        Convergence_curve[l] = Alpha_score

        if l % 1 == 0:
            print(["At iteration " + str(l) + " the best fitness is " + str(Alpha_score)])

        centroid_all = numpy.mean(Positions, axis=0)
        centroid_leaders = (Alpha_pos + Beta_pos + Delta_pos) / 3

        if l % 10 == 0 and l != 0:
            regular_wolves_indices = [i for i in range(SearchAgents_no) if i not in [alpha_index, beta_index, delta_index]]
            
            if len(regular_wolves_indices) > 0:  
 
                movement_vector = centroid_leaders - centroid_all
                learning_rate = 1
                
                # s.movement_vectors.append(movement_vector)

                Positions[regular_wolves_indices] += learning_rate * movement_vector

                for i in regular_wolves_indices:
                    Positions[i, :] = numpy.clip(Positions[i, :], lb, ub)
        
        centroid_all_distance = distance_to_optimum(centroid_all,0)
        centroid_leaders_distance = distance_to_optimum(centroid_leaders,0)
        
        # s.centroid_all.append(centroid_all)
        # s.centroid_leaders.append(centroid_leaders)
        s.centroid_all_distance.append(centroid_all_distance)
        s.centroid_leaders_distance.append(centroid_leaders_distance)

    timerEnd = time.time()
    s.endTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime = timerEnd - timerStart
    s.convergence = Convergence_curve
    s.optimizer = "GWO_modified_v1"
    s.bestIndividual = Alpha_pos
    s.objfname = objf.__name__

    return s
