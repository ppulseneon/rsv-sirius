import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import joblib

data = pd.read_csv('reporn_submit.csv', sep =';')
df = data #.iloc[:, [1, 2]]
print(df)
# df.to_csv('reporn.csv', sep=';', index = False)

df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.lower()
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('кг', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('г', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('л', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('жб', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('шт', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('/', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('/', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('\d+', '')
df.loc[:, 'Наименование товара'] = df['Наименование товара'].str.replace('[a-zA-Z]', '')

'''
X_train, X_valid, y_train, y_valid = train_test_split(df['Наименование товара'], df['Категория продукта'], test_size=0.1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

sgd_ppl_clf = Pipeline([
     ('tfidf', TfidfVectorizer()),
     ('sgd_clf', SGDClassifier(random_state=42))])

sgd_ppl_clf.fit(X_train, y_train)

model_name = 'model2.pkl'
joblib.dump(sgd_ppl_clf, model_name)
print(f'{model_name} saved')
'''

X_train, X_valid, y_train, y_valid = train_test_split(df['Наименование товара'], df['Категория продукта'], test_size=0.1, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=0)

'''
# Преобразование текстовых данных в матрицу TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Обучение модели классификации
classifier = MultinomialNB()
classifier.fit(X_train_tfidf, y_train)

'''
pipeline = Pipeline([
     ('tfidf', TfidfVectorizer()),
     ('sgd_clf', SGDClassifier(random_state=42))])

pipeline.fit(X_train, y_train)

joblib.dump(pipeline, 'model_submit.pkl')
print('yes')