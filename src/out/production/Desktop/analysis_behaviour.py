import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

NUM_PART = 15

df = pd.read_csv("final_data/mind_wandering/_behavior_001.csv", sep = "|")
# y_angle = np.zeros(len(list(df0['steerAngle'])))
# y_pos = np.zeros(len(list(df0['steerAngle'])))
# for i in range(1, 9, 1):
#     name = "data/_behavior_00" + str(i) + ".csv"
#     df_temp = pd.read_csv(name, sep = "|")
#     y_angle += np.array(df_temp['steerAngle'])
#     y_pos_temp = []
#     for elem in df_temp['simcarPos']:
#         y_pos_temp.append(eval(elem))
#     y_pos_temp = [elem[1] for elem in y_pos_temp]
#     y_pos += y_pos_temp
#
# for i in range(10, NUM_PART + 1, 1):
#     name = "data/_behavior_0" + str(i) + ".csv"
#     df_temp = pd.read_csv(name, sep = "|")
#     y_angle += np.array(df_temp['steerAngle'])
#     y_pos_temp = []
#     for elem in df_temp['simcarPos']:
#         y_pos_temp.append(eval(elem))
#     y_pos_temp = [elem[1] for elem in y_pos_temp]
#     y_pos += y_pos_temp
#
# y_angle = y_angle / NUM_PART
# y_pos = y_pos / NUM_PART

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.tight_layout()

y_angle = list(df['steerAngle'][::50])
# transform from radians to degrees
for i in range(len(y_angle)):
    y_angle[i] = y_angle[i] * 180/math.pi

y_pos = []
for elem in df['simcarPos'][::50]:
    y_pos.append(eval(elem))
y_pos = [elem[1] for elem in y_pos]

x = [i * 2.5 for i in range(len(y_angle))]

ax1.plot(x, y_pos)
ax1.axhline(y=0, color='gray', linestyle='--')
ax1.set_ylim([-2, 2])
ax1.set_title("Lane deviation")
ax1.set_ylabel("Meter")
ax1.set_xlabel("time (sec)")


ax2.plot(x, y_angle)
ax2.axhline(y=0, color='gray', linestyle='--')
# ax2.set_ylim([-2, 2])
ax2.set_title("Steering angle")
ax2.set_ylabel("Degrees")
ax2.set_xlabel("time (sec)")

plt.tight_layout()
plt.savefig('final_data/IMAGES/AllGraphs/behaviour_mw.png')
plt.show()



