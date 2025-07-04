# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:50:25 2016

@author: hossam
"""
from pathlib import Path
import EvoloPy.optimizers.PSO as pso
import EvoloPy.optimizers.MVO as mvo
import EvoloPy.optimizers.GWO as gwo
import EvoloPy.optimizers.MFO as mfo
import EvoloPy.optimizers.CS as cs
import EvoloPy.optimizers.BAT as bat
import EvoloPy.optimizers.WOA as woa
import EvoloPy.optimizers.FFA as ffa
import EvoloPy.optimizers.SSA as ssa
import EvoloPy.optimizers.GA as ga
import EvoloPy.optimizers.HHO as hho
import EvoloPy.optimizers.SCA as sca
import EvoloPy.optimizers.JAYA as jaya
import EvoloPy.optimizers.DE as de
import EvoloPy.optimizers.GWO_modified_v1 as gwo_modified_v1
import EvoloPy.optimizers.GWO_modified_v2 as gwo_modified_v2
from EvoloPy import benchmarks
import csv
import numpy
import time
import warnings
import os
from EvoloPy import plot_convergence
from EvoloPy import plot_boxplot

warnings.simplefilter(action="ignore")


def selector(algo, func_details, popSize, Iter):
    function_name = func_details[0]
    lb = func_details[1]
    ub = func_details[2]
    dim = func_details[3]

    if algo == "SSA":
        x = ssa.SSA(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "PSO":
        x = pso.PSO(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "GA":
        x = ga.GA(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "BAT":
        x = bat.BAT(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "FFA":
        x = ffa.FFA(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "GWO":
        x = gwo.GWO(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "WOA":
        x = woa.WOA(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "MVO":
        x = mvo.MVO(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "MFO":
        x = mfo.MFO(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "CS":
        x = cs.CS(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "HHO":
        x = hho.HHO(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "SCA":
        x = sca.SCA(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "JAYA":
        x = jaya.JAYA(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "DE":
        x = de.DE(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "GWO_modified_v1":
        x = gwo_modified_v1.GWO_modified_v1(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    elif algo == "GWO_modified_v2":
        x = gwo_modified_v2.GWO_modified_v2(getattr(benchmarks, function_name), lb, ub, dim, popSize, Iter)
    else:
        return None
    return x


def run(optimizer, objectivefunc, NumOfRuns, params, export_flags):

    """
    It serves as the main interface of the framework for running the experiments.

    Parameters
    ----------
    optimizer : list
        The list of optimizers names
    objectivefunc : list
        The list of benchmark functions
    NumOfRuns : int
        The number of independent runs
    params  : set
        The set of parameters which are:
        1. Size of population (PopulationSize)
        2. The number of iterations (Iterations)
    export_flags : set
        The set of Boolean flags which are:
        1. Export (Exporting the results in a file)
        2. Export_details (Exporting the detailed results in files)
        3. Export_convergence (Exporting the covergence plots)
        4. Export_boxplot (Exporting the box plots)

    Returns
    -----------
    N/A
    """

    # Select general parameters for all optimizers (population size, number of iterations) ....
    PopulationSize = params["PopulationSize"]
    Iterations = params["Iterations"]

    # Export results ?
    Export = export_flags["Export_avg"]
    Export_details = export_flags["Export_details"]
    Export_convergence = export_flags["Export_convergence"]
    Export_boxplot = export_flags["Export_boxplot"]

    Flag = False
    Flag_details = False

    # CSV Header for for the cinvergence
    CnvgHeader = []

    results_directory = time.strftime("%Y-%m-%d-%H-%M-%S") + "/"
    Path(results_directory).mkdir(parents=True, exist_ok=True)

    for l in range(0, Iterations):
        CnvgHeader.append("Iter" + str(l + 1))

    for i in range(0, len(optimizer)):
        for j in range(0, len(objectivefunc)):
            convergence = [0] * NumOfRuns
            executionTime = [0] * NumOfRuns
            # centroid_all_data = [0] * NumOfRuns  
            # centroid_leaders_data = [0] * NumOfRuns  
            centroid_all_distance_data = [0] * NumOfRuns  
            centroid_leaders_distance_data = [0] * NumOfRuns  
            # movement_vectors = [0] * NumOfRuns

            for k in range(0, NumOfRuns):
                func_details = benchmarks.getFunctionDetails(objectivefunc[j])
                x = selector(optimizer[i], func_details, PopulationSize, Iterations)
                convergence[k] = x.convergence
                optimizerName = x.optimizer
                objfname = x.objfname

                # centroid_all_data[k] = x.centroid_all
                # centroid_leaders_data[k] = x.centroid_leaders
                centroid_all_distance_data[k] = x.centroid_all_distance
                centroid_leaders_distance_data[k] = x.centroid_leaders_distance
                # movement_vectors[k] = x.movement_vectors

                if Export_details == True:
                    ExportToFile = results_directory + "experiment_details.csv"
                    with open(ExportToFile, "a", newline="\n") as out:
                        writer = csv.writer(out, delimiter=",")
                        if (
                            Flag_details == False
                        ):  # just one time to write the header of the CSV file
                            header = numpy.concatenate(
                                [["Optimizer", "objfname", "ExecutionTime", "Individual"], CnvgHeader]
                            )
                            writer.writerow(header)
                            Flag_details = True  # at least one experiment
                        executionTime[k] = x.executionTime
                        a = numpy.array([x.optimizer, x.objfname, x.executionTime, x.bestIndividual] + x.convergence.tolist(), dtype=object)
                        writer.writerow(a)
                    out.close()
                    
            
            #average centorid
            if Export_details and NumOfRuns > 0:

                # avg_centroid_all = numpy.mean(numpy.array(centroid_all_data), axis=0)
                # avg_centroid_leaders =  numpy.mean(numpy.array(centroid_leaders_data), axis=0)
                avg_centroid_all_distance =  numpy.mean(numpy.array(centroid_all_distance_data), axis=0)
                avg_centroid_leaders_distance =  numpy.mean(numpy.array(centroid_leaders_distance_data), axis=0)

                avg_centroid_filename = results_directory + f"avg_centroid_details_{optimizer[i]}_{objectivefunc[j]}.csv"
                with open(avg_centroid_filename, "w", newline="\n") as avg_file:
                    writer = csv.writer(avg_file)
                    writer.writerow(["Iteration", "Avg_Centroid_All_Distance", "Avg_Centroid_Leaders_Distance"])
                    for iter_num in range(len(avg_centroid_all_distance)):
                        writer.writerow([
                            (iter_num+1),
                            float(avg_centroid_all_distance[iter_num]),  
                            float(avg_centroid_leaders_distance[iter_num]),  
                            # list(avg_centroid_all[iter_num]), 
                            # list(avg_centroid_leaders[iter_num]), 
                        ])

            # if Export_details == True:
            #     movement_vectors_filename = results_directory + f"movement_vectors_{optimizer[i]}_{objectivefunc[j]}_run{k+1}.csv"
            #     with open(movement_vectors_filename, "w", newline="\n") as mv_file:
            #         writer = csv.writer(mv_file)
            #         writer.writerow(["Iteration", "Movement_Vector"])

            #         for iter_num, vector in enumerate(x.movement_vectors, 1):  
            #             writer.writerow([iter_num, list(vector)])  

            if Export == True:
                ExportToFile = results_directory + "experiment.csv"

                with open(ExportToFile, "a", newline="\n") as out:
                    writer = csv.writer(out, delimiter=",")
                    if (
                        Flag == False
                    ):  # just one time to write the header of the CSV file
                        header = numpy.concatenate(
                            [["Optimizer", "objfname", "ExecutionTime"], CnvgHeader]
                        )
                        writer.writerow(header)
                        Flag = True

                    avgExecutionTime = float("%0.2f" % (sum(executionTime) / NumOfRuns))
                    avgConvergence = numpy.around(
                        numpy.mean(convergence, axis=0, dtype=numpy.float64), decimals=2
                    ).tolist()
                    a = numpy.concatenate([[optimizerName, objfname, avgExecutionTime], avgConvergence])
                    writer.writerow(a)
                out.close()

    if Export_convergence == True:
        plot_convergence.run(results_directory, optimizer, objectivefunc, Iterations)

    if Export_boxplot == True:
        plot_boxplot.run(results_directory, optimizer, objectivefunc, Iterations)

    if Flag == False:  # Faild to run at least one experiment
        print(
            "No Optomizer or Cost function is selected. Check lists of available optimizers and cost functions"
        )

    print("Execution completed")
