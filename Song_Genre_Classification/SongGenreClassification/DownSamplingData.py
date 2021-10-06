import pandas as pd
from sklearn.utils import shuffle

filename = '/Users/asmitasingla/Desktop/MSCSS/Quarter-2/Information-Retrieval/Project/Dataset/ProcessedLyrics.csv'
originalDf = pd.read_csv(filename)
originalDf = originalDf.dropna()
downSampledDF = pd.DataFrame()

# Down sample the data-set to make all genres of equal size
downSampledDF = originalDf.groupby('genre')
downSampledDF = downSampledDF.apply(lambda x: x.sample(downSampledDF.size().min()).reset_index(drop=True))
downSampledDF = shuffle(downSampledDF)
downSampledDF.to_csv('/Users/asmitasingla/Desktop/MSCSS/Quarter-2/Information-Retrieval/Project/Dataset/DownSampledData.csv')
