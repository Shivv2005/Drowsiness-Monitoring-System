import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("drowsiness_log.csv")

plt.plot(data["score"])
plt.title("Sleepiness Over Time")
plt.xlabel("Entry")
plt.ylabel("Score")
plt.show()
