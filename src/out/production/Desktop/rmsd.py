from math import sqrt
from enum import Enum

class TypeGraph(Enum):
    LaneDevMean = 1
    LaneDevSD = 2
    LaneDevMax = 3
    DirChangeCount = 4
    SteerAngleMean = 5


human_single = {TypeGraph.LaneDevMean: 0.506, TypeGraph.LaneDevSD: 0.61, TypeGraph.LaneDevMax: 1.353,
                TypeGraph.DirChangeCount: 225.443, TypeGraph.SteerAngleMean: 4.087}
human_listen = {TypeGraph.LaneDevMean: 0.487, TypeGraph.LaneDevSD: 0.587, TypeGraph.LaneDevMax: 1.323,
                TypeGraph.DirChangeCount: 208.165, TypeGraph.SteerAngleMean: 3.816}

model_single = {TypeGraph.LaneDevMean: 1.396, TypeGraph.LaneDevSD: 2.526, TypeGraph.LaneDevMax: 16.146,
                TypeGraph.DirChangeCount: 229.875, TypeGraph.SteerAngleMean: 21.045}
model_listen_m1 = {TypeGraph.LaneDevMean: 0.167, TypeGraph.LaneDevSD: 0.133, TypeGraph.LaneDevMax: 0.871,
                   TypeGraph.DirChangeCount: 213.291, TypeGraph.SteerAngleMean: 5.657}
model_listen_m2 = {TypeGraph.LaneDevMean: 1.693, TypeGraph.LaneDevSD: 1.244, TypeGraph.LaneDevMax: 6.597,
                   TypeGraph.DirChangeCount: 196.333, TypeGraph.SteerAngleMean: 36.334}
model_listen_m3 = {TypeGraph.LaneDevMean: 0.425, TypeGraph.LaneDevSD: 0.332, TypeGraph.LaneDevMax: 1.917,
                   TypeGraph.DirChangeCount: 220.166, TypeGraph.SteerAngleMean: 14.572}
model_listen_m4 = {TypeGraph.LaneDevMean: 0.619, TypeGraph.LaneDevSD: 0.642, TypeGraph.LaneDevMax: 4.24,
                   TypeGraph.DirChangeCount: 219.208, TypeGraph.SteerAngleMean: 18.445}



def rmsd(human_single, model_single, human_listen, model_listen):
    return sqrt(abs(human_single - model_single)**2 + abs(human_listen - model_listen)**2)

for graph in TypeGraph:
    print("##########################", graph)
    print("Listen m1: ", rmsd(human_single[graph], model_single[graph], human_listen[graph], model_listen_m1[graph]))
    print("Listen m2: ", rmsd(human_single[graph], model_single[graph], human_listen[graph], model_listen_m2[graph]))
    print("Listen m3: ", rmsd(human_single[graph], model_single[graph], human_listen[graph], model_listen_m3[graph]))
    print("Listen m4: ", rmsd(human_single[graph], model_single[graph], human_listen[graph], model_listen_m4[graph]))

# import pandas as pd
#
# folder_dr = "driving"
# folder_mw = "mind_wandering"
# folder_listen_m1 = "listen_m1"
# folder_listen_m2 = "listen_m2"
# folder_listen_m3 = "listen_m3"
# folder_listen_m4 = "listen_m4"
#
# def func(folder):
#     for i in range(1, 11, 1):
#         try:
#             name = "final_data/" + folder + "/_behavior_00" + str(i) + ".csv"
#             df_temp = pd.read_csv(name, sep="|")
#         except FileNotFoundError:
#             name = "final_data/" + folder + "/_behavior_0" + str(i) + ".csv"
#             df_temp = pd.read_csv(name, sep="|")
#
#         pos = []
#         for elem in df_temp['simcarPos']:
#             try:
#                 pos.append(eval(elem))
#             except NameError:
#                 pass
#         pos = [elem[1] for elem in pos]
#
#         df_temp['simcarPos_y'] = pos
#         df_temp.to_csv(name, sep="|")
#
# func(folder_listen_m1)
# func(folder_listen_m2)
# func(folder_listen_m3)
# func(folder_listen_m4)