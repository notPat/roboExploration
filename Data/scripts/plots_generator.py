import pandas as pd
import matplotlib.pyplot as plt
import os


global_df = pd.read_csv("ExploredSectorsOverTime.csv")

robots = []
robot_ids = []

for i in range(10):
    filename = f"ExploredSectorsOverTime_Robot {i}.csv"
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        robots.append(df)
        robot_ids.append(i)

plt.figure()

plt.plot(global_df["Time"], global_df["SektorsGained"], label="Global")

for i, df in zip(robot_ids, robots):
    plt.plot(df["Time"], df[df.columns[1]], label=f"Robot {i}")

plt.xlabel("Zeit in Sekunden")
plt.ylabel("Erkundete Sektoren")
plt.title("Erkundungs Verlauf")
plt.legend()

graphname = f"sewer-frontier-{len(robots)}bots.png"

plt.savefig(graphname, dpi=300)
plt.show()