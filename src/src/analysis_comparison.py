# listen model 1: always attend, no access meaning
# listen model 2: always attend, access meaning
# listen model 3: attend while wandering, access meaning
# listen model 4: always attend, access meaning while wandering
import math

import pandas as pd
from statistics import mean, stdev
import statistics
from math import sqrt
import matplotlib.pyplot as plt
from enum import Enum

# compute the mean/max/stdev lane deviation of 25 model runs
def get_lane_dev(folder, measure):
    lane_dev = []
    for i in range(1, 25, 1):
        try:
            name = "final_data/" + folder + "/_behavior_00" + str(i) + ".csv"
            df_temp = pd.read_csv(name, sep="|")
        except FileNotFoundError:
            name = "final_data/" + folder + "/_behavior_0" + str(i) + ".csv"
            df_temp = pd.read_csv(name, sep="|")

        pos = []
        for elem in df_temp['simcarPos']:
            try:
                pos.append(eval(elem))
            except NameError:
                pass
        pos = [abs(elem[1]) for elem in pos]
        lane_dev.append(measure(pos))
    return lane_dev

# compute number of direction changes of 25 model runs
def get_change_dir_count(folder):
    change_count = []
    for i in range(1, 25, 1):
        try:
            name = "final_data/" + folder + "/_behavior_00" + str(i) + ".csv"
            df_temp = pd.read_csv(name, sep="|")
        except FileNotFoundError:
            name = "final_data/" + folder + "/_behavior_0" + str(i) + ".csv"
            df_temp = pd.read_csv(name, sep="|")

        pos = []
        for elem in df_temp['simcarPos']:
            try:
                pos.append(eval(elem))
            except NameError:
                pass
        pos = [elem[1] for elem in pos]

        count = 0
        idx = 1
        while idx < len(pos):
            flag = "ascend"
            if pos[idx] < pos[idx - 1]:
                flag = "descend"

            while idx < len(pos):
                if flag == "ascend":
                    if pos[idx] < pos[idx - 1]:
                        break

                else:
                    if pos[idx] > pos[idx - 1]:
                        break

                idx += 1
            count += 1

        change_count.append(count)
    return change_count

# compute the mean angle devviation of steering angle of 25 model runs
def get_steer_angle_mean(folder):
    steer_angle = []
    for i in range(1, 25, 1):
        try:
            name = "final_data/" + folder + "/_behavior_00" + str(i) + ".csv"
            df_temp = pd.read_csv(name, sep="|")
        except FileNotFoundError:
            name = "final_data/" + folder + "/_behavior_0" + str(i) + ".csv"
            df_temp = pd.read_csv(name, sep="|")

        angle_list = []
        for elem in df_temp['steerAngle']:
            try:
                angle_list.append(abs(float(elem)) * 180/math.pi)
            except ValueError:
                pass
        steer_angle.append(mean(angle_list))
    return steer_angle

# compute mean and confidence interval
def plot_confidence_interval(name, x, values, z=1.96, color='black', horizontal_line_width=0.25):
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    confidence_interval = z * stdev / sqrt(len(values))
    print(name, mean)

    left = x - horizontal_line_width / 2
    top = mean - confidence_interval
    right = x + horizontal_line_width / 2
    bottom = mean + confidence_interval
    plt.plot([top, bottom], [x, x], color=color)
    plt.plot([top, top], [left, right], color=color)
    plt.plot([bottom, bottom], [left, right], color=color)
    plt.plot(mean, x, 'o', color='black')

    return mean, confidence_interval

# main plotting function
def process_graph(graph):
    try:
        func, opt, label, title = graph.value[0], graph.value[1], graph.value[2], graph.value[3]

        lane_dev_driving = func(folder_dr, opt)
        lane_dev_mw = func(folder_mw, opt)
        lane_dev_mw_listen_m1 = func(folder_listen_m1, opt)
        lane_dev_mw_listen_m2 = func(folder_listen_m2, opt)
        lane_dev_mw_listen_m3 = func(folder_listen_m3, opt)
        lane_dev_mw_listen_m4 = func(folder_listen_m4, opt)

    except IndexError:
        func, label, title = graph.value[0], graph.value[1], graph.value[2]

        lane_dev_driving = func(folder_dr)
        lane_dev_mw = func(folder_mw)
        lane_dev_mw_listen_m1 = func(folder_listen_m1)
        lane_dev_mw_listen_m2 = func(folder_listen_m2)
        lane_dev_mw_listen_m3 = func(folder_listen_m3)
        lane_dev_mw_listen_m4 = func(folder_listen_m4)

    data = [lane_dev_mw_listen_m4, lane_dev_mw_listen_m3, lane_dev_mw_listen_m2, lane_dev_mw_listen_m1, lane_dev_mw, lane_dev_driving]

    fig, ax = plt.subplots()

    ax.axhline(y=1, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=2, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=3, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=4, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=5, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=6, color='black', linestyle='--', alpha=0.25)

    r = ax.violinplot(data, vert=False, showmeans=False, showextrema=False)
    for pc in r['bodies']:
        pc.set_facecolor('#D3D3D3')
        pc.set_alpha(1)
    ax.set_title(title, fontsize=15)

    if label == "Speed (km/h)":
        plt.xlim(20, 30)

    ax.set_xlabel(label, fontsize=12)
    plt.xticks(fontsize=11)
    ax.set_yticks([6, 5, 4, 3, 2, 1])
    ax.set_yticklabels(["Baseline\nSalvucci", "Single\n(MW)", "MW+\nListen1", "MW+\nListen2", "MW+\nListen3", "MW+\nListen4"], fontsize=12)


    plot_confidence_interval("Drive", 6, lane_dev_driving)
    plot_confidence_interval("MW", 5, lane_dev_mw)
    plot_confidence_interval("Listen_m1", 4, lane_dev_mw_listen_m1)
    plot_confidence_interval("Listen_m2", 3, lane_dev_mw_listen_m2)
    plot_confidence_interval("Listen_m3", 2, lane_dev_mw_listen_m3)
    plot_confidence_interval("Listen_m4", 1, lane_dev_mw_listen_m4)
    return plt

# TypeGraph = [function to compute, (optional) metric, name of y axis, title of figure]
class TypeGraph(Enum):
    LaneDevMean = [get_lane_dev, mean, "Deviation (meter)", "Mean Lane Deviation"]
    LaneDevSD = [get_lane_dev, stdev, "Deviation (meter)", "SD Lane Deviation"]
    LaneDevMax = [get_lane_dev, max, "Deviation (meter)", "Max Lane Deviation"]
    DirChangeCount = [get_change_dir_count, "Count", "Count of Direction Changes"]
    SteerAngleMean = [get_steer_angle_mean, "Degrees", "Mean Steer Angle"]


if __name__ == '__main__':
    # folder paths
    folder_dr = "driving"
    folder_mw = "mind_wandering"
    folder_listen_m1 = "listen_m1"
    folder_listen_m2 = "listen_m2"
    folder_listen_m3 = "listen_m3"
    folder_listen_m4 = "listen_m4"
    # True if all graphs generated at once
    generateAllGraphs = True

    if generateAllGraphs:
        for graph in TypeGraph:
            plt = process_graph(graph)
            plt.savefig(f"final_data/IMAGES/AllGraphs/{graph.name}.png")

            print(f"Graph {graph.name} created!")

    else:
        # specify type of graph to be generated
        graph = TypeGraph.SteerAngleMean
        plt = process_graph(graph)
        plt.show()









