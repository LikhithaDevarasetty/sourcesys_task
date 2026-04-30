# ==========================================
# Matplotlib Complete Practice (With Titles)
# ==========================================

import matplotlib.pyplot as plt
import numpy as np

# 1. Basic Line Plot
x = [1,2,3,4]
y = [2,4,1,5]
plt.plot(x,y)
plt.title("1. Basic Line Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

# 2. Styled Line
x = np.linspace(0,10,100)
plt.plot(x,np.sin(x),label="sin",linestyle='-',marker='o')
plt.plot(x,np.cos(x),label="cos",linestyle='--')
plt.title("2. Styled Line Plot")
plt.legend(); plt.grid()
plt.show()

# 3. Scatter
plt.scatter(np.random.randn(50), np.random.randn(50))
plt.title("3. Scatter Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

# 4. Bar
plt.bar(["A","B","C"],[5,7,3])
plt.title("4. Bar Chart")
plt.xlabel("Category")
plt.ylabel("Values")
plt.show()

# 5. Horizontal Bar
plt.barh(["A","B","C"],[5,7,3])
plt.title("5. Horizontal Bar Chart")
plt.xlabel("Values")
plt.ylabel("Category")
plt.show()

# 6. Grouped Bar
x = np.arange(3)
plt.bar(x-0.2,[5,6,7],width=0.4,label="2023")
plt.bar(x+0.2,[6,7,8],width=0.4,label="2024")
plt.title("6. Grouped Bar Chart")
plt.legend()
plt.show()

# 7. Stacked Bar
a=[3,4,5]; b=[2,3,4]
plt.bar(["A","B","C"],a,label="Part1")
plt.bar(["A","B","C"],b,bottom=a,label="Part2")
plt.title("7. Stacked Bar Chart")
plt.legend()
plt.show()

# 8. Pie
plt.pie([40,30,30],labels=["A","B","C"],autopct='%1.1f%%')
plt.title("8. Pie Chart")
plt.show()

# 9. Histogram
data=np.random.normal(60,10,100)
plt.hist(data,bins=10)
plt.title("9. Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# 10. Boxplot
plt.boxplot([np.random.randn(50),np.random.randn(50)])
plt.title("10. Box Plot")
plt.show()

# 11. Area
x=np.linspace(0,5,100)
plt.fill_between(x,np.sin(x))
plt.title("11. Area Plot")
plt.show()

# 12. Subplots
x=np.linspace(0,10,100)
fig,ax=plt.subplots(2,1)
ax[0].plot(x,np.sin(x))
ax[0].set_title("sin(x)")
ax[1].plot(x,np.cos(x))
ax[1].set_title("cos(x)")
plt.suptitle("12. Subplots Example")
plt.show()

# 13. Twin Axis
fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar([1,2,3],[10,20,30])
ax2.plot([1,2,3],[1,2,3])
plt.title("13. Twin Axis Plot")
plt.show()

# 14. Annotation
x=np.linspace(0,10,100)
y=np.sin(x)
plt.plot(x,y)
plt.annotate("Peak",xy=(1.5,1))
plt.title("14. Annotation Example")
plt.show()

# 15. Step Plot
plt.step([1,2,3,4],[2,3,5,4])
plt.title("15. Step Plot")
plt.show()

# 16. Stem Plot
plt.stem([1,2,3],[2,3,4])
plt.title("16. Stem Plot")
plt.show()

# 17. Heatmap
plt.imshow(np.random.randint(1,10,(5,5)))
plt.colorbar()
plt.title("17. Heatmap")
plt.show()

# 18. Contour
x=np.linspace(-3,3,50)
y=np.linspace(-3,3,50)
X,Y=np.meshgrid(x,y)
Z=np.sin(X)*np.cos(Y)
plt.contour(X,Y,Z)
plt.title("18. Contour Plot")
plt.show()

# 19. Filled Contour
plt.contourf(X,Y,Z)
plt.title("19. Filled Contour Plot")
plt.show()

# 20. 3D Plot
from mpl_toolkits.mplot3d import Axes3D
fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.plot_surface(X,Y,Z)
plt.title("20. 3D Surface Plot")
plt.show()

# 21. Polar Plot
theta=np.linspace(0,2*np.pi,100)
r=1+np.sin(theta)
plt.polar(theta,r)
plt.title("21. Polar Plot")
plt.show()

# 22. Error Bars
x=np.arange(5)
y=[2,3,4,5,6]
err=[0.2,0.3,0.1,0.4,0.2]
plt.errorbar(x,y,yerr=err)
plt.title("22. Error Bar Plot")
plt.show()

# 23. Violin Plot
plt.violinplot([np.random.randn(100),np.random.randn(100)])
plt.title("23. Violin Plot")
plt.show()

# 24. Hexbin
x=np.random.randn(500)
y=x+np.random.randn(500)
plt.hexbin(x,y)
plt.colorbar()
plt.title("24. Hexbin Plot")
plt.show()

# 25. Log Scale
x=np.logspace(0,3,100)
plt.plot(x,x**2)
plt.xscale('log'); plt.yscale('log')
plt.title("25. Log Scale Plot")
plt.show()

# 26. Custom Figure
plt.figure(figsize=(6,3))
plt.plot(np.sin(np.linspace(0,10,100)))
plt.title("26. Custom Figure Size")
plt.show()

# 27. Multiple Legends
x=np.linspace(0,10,100)
l1,=plt.plot(x,np.sin(x))
l2,=plt.plot(x,np.cos(x))
plt.legend([l1,l2],["sin","cos"])
plt.title("27. Multiple Legends")
plt.show()

# 28. GridSpec Layout
import matplotlib.gridspec as gridspec
fig=plt.figure()
gs=gridspec.GridSpec(2,2)
plt.subplot(gs[0,0]); plt.plot([1,2]); plt.title("Plot 1")
plt.subplot(gs[1,:]); plt.plot([3,4]); plt.title("Plot 2")
plt.suptitle("28. GridSpec Layout")
plt.show()

# 29. Tick Customization
x=np.linspace(0,100,100)
plt.plot(x,np.sin(x))
plt.xticks(np.arange(0,101,20))
plt.title("29. Tick Customization")
plt.show()

# 30. Shapes (Patch)
import matplotlib.patches as patches
fig,ax=plt.subplots()
circle=patches.Circle((0.5,0.5),0.2)
ax.add_patch(circle)
plt.xlim(0,1); plt.ylim(0,1)
plt.title("30. Shapes (Circle)")
plt.show()

print("All concepts covered with titles ✅")