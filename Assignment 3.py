import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import scipy.optimize as opt
import err_ranges as err




url = 'API_19_DS2_en_csv_v2_4773766.csv'
indicator = 'Climate change'
year1 = '2000'
year2 = '2020'

df = pd.read_csv(url, skiprows=4)
df = df.loc[df['Indicator Name'] == indicator]

#extract the required data for the clustering
df_cluster = df.loc[df.index, ['Country Name', year1, year2]]

#convert the datafram to an array
x = df_cluster[[year1, year2]].dropna().values

df_cluster = df_cluster.sort_values(year1, ascending=False)
print(df_cluster.head(5))

print(x)

df_cluster.plot(year1, year2, kind='scatter')

sse = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(x)
    sse.append(kmeans.inertia_)

plt.plot(range(1, 11), sse)
plt.savefig('clusters.png')
plt.show()

kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, n_init=10, random_state=0)
y_kmeans = kmeans.fit_predict(x)

print(y_kmeans)

plt.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 1], s = 50, c = 'purple',label = 'label 0')
plt.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 1], s = 50, c = 'orange',label = 'label 1')
plt.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 1], s = 50, c = 'green',label = 'label 2')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], s = 10, c = 'red', label = 'Centroids')
plt.legend()
plt.show()



#Fitting 
def model(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

#transpose of original data
df_year = df.T

#rename the columns
df_year = df_year.rename(columns=df_year.iloc[0])

#drop the country name
df_year = df_year.drop(index=df_year.index[0], axis=0)
df_year['Year'] = df_year.index

df_fitting = df_year[['Year', 'Canada']].apply(pd.to_numeric, errors='coerce')

m = df_fitting.dropna().values

x_axis = m[:,0]
y_axis = m[:,1]

#x_axis y_axis = m[:,0], m[:,1]
popt, _ = opt.curve_fit(model, x_axis, y_axis)
param, covar = opt.curve_fit(model, x_axis, y_axis)
a, b, c, d = popt

sigma = np.sqrt(np.diag(covar))
low, up = err.err_ranges(m, model, popt, sigma)
plt.scatter(x_axis, y_axis)


x_line = np.arange(min(m[:,0]), max(m[:,0])+1, 1)
y_line = model(x_line, a, b, c, d)

#print('low',low, 'up',up)
print(up.shape)


plt.scatter(x_axis, y_axis)
plt.plot(x_line, y_line, '--', color='black')
plt.fill_between(m, low, up, alpha=0.7, color='green')
plt.show()



