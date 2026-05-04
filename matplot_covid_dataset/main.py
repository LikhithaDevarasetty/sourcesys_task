import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv("covid-19 data.csv")

df = df.sort_values(by="confirmed", ascending=False).head(10)

# 1. Line Plot
plt.plot(df["country"], df["confirmed"])
plt.title("1. Confirmed Cases (Top 10 Countries)")
plt.xticks(rotation=45)
plt.show()


# 2. Styled Line
plt.plot(df["country"], df["confirmed"], marker='o', label="Confirmed")
plt.plot(df["country"], df["deaths"], marker='s', label="Deaths")
plt.legend()
plt.title("2. Confirmed vs Deaths")
plt.xticks(rotation=45)
plt.show()


# 3. Scatter
plt.scatter(df["confirmed"], df["deaths"])
plt.xlabel("Confirmed")
plt.ylabel("Deaths")
plt.title("3. Confirmed vs Deaths Scatter")
plt.show()


# 4. Bar
plt.bar(df["country"], df["confirmed"])
plt.xticks(rotation=45)
plt.title("4. Confirmed Cases Bar Chart")
plt.show()


# 5. Horizontal Bar
plt.barh(df["country"], df["deaths"])
plt.title("5. Death Cases")
plt.show()


# 6. Grouped Bar
x = np.arange(len(df))
plt.bar(x-0.2, df["confirmed"], width=0.4, label="Confirmed")
plt.bar(x+0.2, df["recovered"], width=0.4, label="Recovered")
plt.xticks(x, df["country"], rotation=45)
plt.legend()
plt.title("6. Confirmed vs Recovered")
plt.show()


# 7. Stacked Bar
plt.bar(df["country"], df["confirmed"])
plt.bar(df["country"], df["recovered"], bottom=df["confirmed"])
plt.xticks(rotation=45)
plt.title("7. Stacked Chart")
plt.show()


# 8. Pie Chart
plt.pie(df["confirmed"], labels=df["country"], autopct='%1.1f%%')
plt.title("8. Confirmed Distribution")
plt.show()


# 9. Histogram
plt.hist(df["confirmed"], bins=5)
plt.title("9. Confirmed Distribution")
plt.show()


# 10. Box Plot
plt.boxplot(df["confirmed"])
plt.title("10. Boxplot")
plt.show()


# 11. Area Plot
plt.fill_between(range(len(df)), df["confirmed"])
plt.title("11. Area Plot")
plt.show()


# 12. Subplots
fig, ax = plt.subplots(2,1)
ax[0].plot(df["confirmed"])
ax[0].set_title("Confirmed")
ax[1].plot(df["deaths"])
ax[1].set_title("Deaths")
plt.show()


# 13. Twin Axis
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(df["confirmed"])
ax2.plot(df["deaths"], color='red')
plt.title("13. Twin Axis")
plt.show()


# 14. Annotation
plt.plot(df["confirmed"])
plt.annotate("Max", xy=(0, df["confirmed"].max()))
plt.title("14. Annotation")
plt.show()


# 15. Step Plot
plt.step(range(len(df)), df["confirmed"])
plt.title("15. Step Plot")
plt.show()


# 16. Stem Plot
plt.stem(df["confirmed"])
plt.title("16. Stem Plot")
plt.show()


# 17. Heatmap
data = df[["confirmed","recovered","deaths","critical"]]
plt.imshow(data, aspect='auto')
plt.colorbar()
plt.title("17. Heatmap")
plt.show()


# 18. Contour
x = np.linspace(0,10,50)
y = np.linspace(0,10,50)
X,Y = np.meshgrid(x,y)
Z = np.sin(X)*np.cos(Y)
plt.contour(X,Y,Z)
plt.title("18. Contour")
plt.show()


# 19. Filled Contour
plt.contourf(X,Y,Z)
plt.title("19. Filled Contour")
plt.show()


# 20. 3D Plot
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(df["confirmed"], df["deaths"], df["recovered"])
plt.title("20. 3D Plot")
plt.show()


# 21. Polar
theta = np.linspace(0,2*np.pi,len(df))
r = df["confirmed"]
plt.polar(theta, r)
plt.title("21. Polar Plot")
plt.show()


# 22. Error Bar
plt.errorbar(range(len(df)), df["confirmed"], yerr=df["deaths"])
plt.title("22. Error Bar")
plt.show()


# 23. Violin Plot
plt.violinplot(df["confirmed"])
plt.title("23. Violin Plot")
plt.show()


# 24. Hexbin
plt.hexbin(df["confirmed"], df["deaths"])
plt.title("24. Hexbin")
plt.show()


# 25. Log Scale
plt.plot(df["confirmed"])
plt.yscale('log')
plt.title("25. Log Scale")
plt.show()


# 26. Custom Figure
plt.figure(figsize=(8,4))
plt.plot(df["confirmed"])
plt.title("26. Custom Size")
plt.show()


# 27. Multiple Legends
l1, = plt.plot(df["confirmed"])
l2, = plt.plot(df["deaths"])
plt.legend([l1,l2],["Confirmed","Deaths"])
plt.title("27. Multiple Legends")
plt.show()


# 28. GridSpec
import matplotlib.gridspec as gridspec
fig = plt.figure()
gs = gridspec.GridSpec(2,2)
plt.subplot(gs[0,0]); plt.plot(df["confirmed"]); plt.title("Confirmed")
plt.subplot(gs[1,:]); plt.plot(df["deaths"]); plt.title("Deaths")
plt.show()


# 29. Ticks
plt.plot(df["confirmed"])
plt.xticks(range(len(df)), df["country"], rotation=45)
plt.title("29. Tick Customization")
plt.show()


# 30. Shapes
import matplotlib.patches as patches
fig, ax = plt.subplots()
circle = patches.Circle((0.5,0.5),0.2)
ax.add_patch(circle)
plt.title("30. Shape Example")
plt.show()

