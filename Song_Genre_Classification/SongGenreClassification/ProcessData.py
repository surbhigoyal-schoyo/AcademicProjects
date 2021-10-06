import ssl
import regex as re
import pandas as pd
import numpy as np
import statistics
import nltk
from nltk.stem.snowball import SnowballStemmer

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
from nltk.corpus import stopwords

filename = '/Users/asmitasingla/Desktop/MSCSS/Quarter-2/Information-Retrieval/Project/Dataset/lyrics.csv'

# Balance the data
print("Balancing the data...")
freq = {}
originalDf = pd.read_csv(filename)
print("Original number of rows: ", originalDf.shape[0])

# Remove rows with genre 'Not Available' and 'Other'
originalDf = originalDf[originalDf.genre != 'Not Available']
originalDf = originalDf[originalDf.genre != 'Other']

for index, row in originalDf.iterrows():
    genre = row['genre']
    if genre in freq:
        freq[genre] += 1
    else:
        freq[genre] = 1
print("Word Frequency: ", freq)

mean_frequency = statistics.mean(freq.values()).__round__()
print("Mean frequency: ", mean_frequency)
drop_table = {}
for k, v in freq.items():
    if v > mean_frequency:
        drop_table[k] = v - mean_frequency
print("Unbalanced words: ", drop_table)
remove_indices = []
for k, v in drop_table.items():
    indices = originalDf[originalDf['genre'] == k].index[0:v]
    remove_indices = np.concatenate([remove_indices, indices])

balancedDf = pd.DataFrame()
balancedDf = originalDf.drop(remove_indices)
balancedDf = balancedDf.dropna()
print("Balanced number of rows: ", balancedDf.shape[0])

freq = {}
for index, row in balancedDf.iterrows():
    genre = row['genre']
    if genre in freq:
        freq[genre] += 1
    else:
        freq[genre] = 1
print("Word Frequency after balancing: ", freq)

# Implement text processing
# Remove Special characters
print("Removing special characters from the lyrics...")
balancedDf['LyricsNoSpecialChar'] = balancedDf['lyrics'].map(lambda x: re.sub(r'\W+', ' ', x))
balancedDf = balancedDf.drop(columns=['lyrics'])

# Implement Stemming
print("Stemming the lyrics...")
stemmer = SnowballStemmer("english")
balancedDf['LyricsNoSpecialChar'] = balancedDf['LyricsNoSpecialChar'].str.split()
balancedDf['StemmedLyrics'] = balancedDf['LyricsNoSpecialChar'].apply(lambda x: [stemmer.stem(y) for y in x])
balancedDf = balancedDf.drop(columns=['LyricsNoSpecialChar'])

# Remove stop words
print("Removing stop words from the lyrics...")
stop = stopwords.words('english')
balancedDf['FinalLyrics'] = balancedDf['StemmedLyrics'].apply(lambda x: ' '.join([word for word in x if word not in stop]))
balancedDf = balancedDf.drop(columns=['StemmedLyrics'])

# Export final data frame to a CSV
print("Exporting final CSV file...")
balancedDf.to_csv('/Users/asmitasingla/Desktop/MSCSS/Quarter-2/Information-Retrieval/Project/Dataset/ProcessedLyrics.csv')
print("Finished")
