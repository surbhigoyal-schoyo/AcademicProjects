import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

array = [[398 ,  4 ,  7 ,  3 , 10 , 10  , 3 , 12 ,  4  , 7],
[172 ,183 ,  4 , 15  ,20 ,  9  ,25 , 24 ,  5 , 18],
[ 97 ,  8 ,306,   2 , 14 ,  8 ,  9 , 10,   4 ,  7],
[ 67 ,  9 ,  5, 321 ,  7  , 3,  10 , 12 ,  4 ,  5],
[137 , 12 ,  4 ,  1 ,244 ,  3  , 8 , 12 ,  5 ,  9],
[128  , 6 ,  6 ,  5 ,  5 ,274 ,  1 , 10 , 13 ,  9],
[ 84  ,18 , 12 ,  9 ,  5 ,  0 ,274 ,  7 ,  2 , 19],
[171  ,21 ,  8 , 21 ,  8 , 10 ,  7, 139 ,  9 , 19],
[130  ,11 ,  2 , 10 ,  4  , 6 , 11 ,  4 ,288 , 11],
[177  ,13 , 11 ,  2 , 22  ,15 , 31  ,13 ,  8 ,155]]

classes = ['Metal', 'Country', 'Jazz', 'Electronic', 'Folk', 'R&B', 'Indie', 'Hip-Hop', 'Pop', 'Rock']

df_cm = pd.DataFrame(array, columns=pd.np.unique(classes), index=pd.np.unique(classes))
plt.figure(figsize=(10, 7))
sn.set(font_scale=1.4)  # for label size
sn.heatmap(df_cm, annot=True, cmap='Blues', fmt='d')  # font size

plt.show()
