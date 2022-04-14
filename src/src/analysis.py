import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/_behavior_004.csv", sep = "|")
fig, (ax1, ax2) = plt.subplots(2)
fig.tight_layout()

y_angle = list(df['steerAngle'])

y_pos = []
for elem in df['simcarPos']:
    y_pos.append(eval(elem))
y_pos = [elem[1] for elem in y_pos]

x = [i for i in range(len(y_angle))]

ax1.plot(x, y_angle)
ax1.axhline(y=0, color='gray', linestyle='--')
ax1.set_title("Steering angle")
# ax1.set_xlabel("time step")


ax2.plot(x, y_pos)
ax2.axhline(y=0, color='gray', linestyle='--')
ax2.set_title("Lane deviation")
# ax2.set_xlabel("time step")

plt.savefig('images/intrusive_004.png')
plt.show()

