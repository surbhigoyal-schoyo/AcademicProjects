import random
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer

# Read the data into a data-frame and selecting the columns we need
from sklearn.naive_bayes import MultinomialNB

directoryPath = "/Users/asmitasingla/Desktop/MSCSS/Quarter-2/Information-Retrieval/Project/Dataset/"
df_lyrics = pd.read_csv(directoryPath + "ProcessedLyrics.csv")

# The following line reads the down-sampled data-set
#df_lyrics = pd.read_csv(directoryPath + "DownSampledData.csv")

df_lyrics = df_lyrics.dropna()

# Concatenate Artist and Final-Lyrics Text
artist = df_lyrics["artist"].copy()
df_lyrics["FinalLyrics"] = df_lyrics["FinalLyrics"].str.cat(artist, sep=" ")
data_lyrics = df_lyrics.loc[:, ['FinalLyrics', 'genre']]

# Split the data into 106455 training instances and 30000 test instances for original data: Total: 136455
n = 30000

# Split the data into 17870 training instances and 4500 test instances for down-sampled data: 22370
#n = 4500

all_Ids = np.arange(len(data_lyrics))
random.shuffle(all_Ids)
test_Ids = all_Ids[0:n]
train_Ids = all_Ids[n:]
data_test = data_lyrics.iloc[test_Ids, :]
data_train = data_lyrics.iloc[train_Ids, :]

# Set the parameters
vocab_size = 10000

# Create the vector of page likes to be sent as input
tfidf_vector = TfidfVectorizer(max_features=vocab_size)
X_train = tfidf_vector.fit_transform(data_train['FinalLyrics'])
y_train = data_train['genre']

# Train the model
model_predict_genre = RandomForestClassifier(n_estimators=30, bootstrap=True, max_features='sqrt', random_state=42)

model_predict_genre.fit(X_train, y_train)

# Predict the genre
X_test = tfidf_vector.transform(data_test['FinalLyrics'])
y_test = data_test['genre']
y_predicted = model_predict_genre.predict(X_test)

# Report mean accuracy using 10 cross validation
mean_accuracy = cross_val_score(model_predict_genre, X_train, y_train, scoring='accuracy', cv=10).mean()
print("Mean of Accuracies measured by 10-Fold Cross Validation:", mean_accuracy)

# Report accuracy and generate confusion matrix
print("Accuracy: %.2f" % accuracy_score(y_test, y_predicted))
classes = ['Metal', 'Country', 'Jazz', 'Electronic', 'Folk', 'R&B', 'Indie', 'Hip-Hop', 'Pop', 'Rock']
cnf_matrix = confusion_matrix(y_test, y_predicted, labels=classes)
print("Confusion matrix:")
print(cnf_matrix)

# Report accuracy using F-score
f_score = f1_score(y_test, y_predicted, average='macro')
print("F-score: ", f_score)
