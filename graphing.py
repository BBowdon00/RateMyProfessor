import seaborn
import pandas
import matplotlib.pyplot as plt

csv = pandas.read_csv(r'test1.csv')
res = seaborn.lineplot(x="Difficulty",y="Quality",data=csv)
plt.show()

