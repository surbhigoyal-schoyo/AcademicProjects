import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the Dataset
directoryPath = "/Users/asmitasingla/Desktop/MSCSS/Quarter-2/Information-Retrieval/Project/Dataset/"
train_df = pd.read_csv(directoryPath + "ProcessedLyrics.csv")

# The following line reads the down-sampled data-set
#train_df = pd.read_csv(directoryPath + "DownSampledData.csv")

train_df.FinalLyrics = train_df.FinalLyrics.astype(str)
train_df.dropna()

# Concatenate Artist and Final-Lyrics Text
artist = train_df["artist"].copy()
train_df["FinalLyrics"] = train_df["FinalLyrics"].str.cat(artist, sep=" ")
data_lyrics = train_df.loc[:, ['FinalLyrics', 'genre']]

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

print(train_df.shape)

train_text = data_train['FinalLyrics']
train_label = data_train['genre']

val_text = data_test['FinalLyrics']
val_label = data_test['genre']

# Encode the labels
encoder = LabelBinarizer()
encoder.fit(train_label)
train_label = encoder.transform(train_label)
encoder.fit(val_label)
val_label = encoder.transform(val_label)

X_train = train_text
y_train = train_label

X_test = val_text
y_test = val_label

# Set the parameters
vocab_size = 10000
max_len = 10000
batch_size = 64
epochs = 5
lr = 0.001

tfidf_vector = TfidfVectorizer(max_features=vocab_size)
X_train = tfidf_vector.fit_transform(train_text).toarray()
X_test = tfidf_vector.transform(val_text).toarray()

print('x_train shape:', X_train.shape)
print('x_test shape:', X_test.shape)
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)

opt = Adam(lr=lr)

# Train the model
genre_model = Sequential()
genre_model.add(Dense(512, input_shape=(vocab_size,), activation='relu'))
genre_model.add(Dropout(0.5))
genre_model.add(Dense(10, activation='softmax'))
genre_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

model_history = genre_model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, y_test))

# Generate confusion matrix
predictions = genre_model.predict(X_test)
y_predict = (predictions > 0.5)
cnf_matrix = confusion_matrix(y_test.argmax(axis=1), y_predict.argmax(axis=1))
print("Confusion matrix:")
print(cnf_matrix)

# Report accuracy using F-score
f_score = f1_score(y_test, y_predict, average='macro')
print("F-score: ", f_score)

# Visualize text_model for accuracy
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Visualize text_model for loss
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
