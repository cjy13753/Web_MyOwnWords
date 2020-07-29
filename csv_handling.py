import pandas as pd
import numpy as np
import mysql.connector

# Create an object to connect to the local MySQL DB Server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    database="test_yourownwords"
    )
cursor = connection.cursor()

# Read an existing csv file containing English vocabs with three columns; words, property, and detail
df = pd.read_csv('WordsCollection.csv')

# Assign matching_id numbers to the dataframe in such a way that one table for words and another for example sentences are created with matching_id numbers connecting the two tables
df['matching_id'] = 0
i = -1
for n in range(df.shape[0]):
    if df.loc[n, 'property'] == '의미:':
        i += 1
        df.loc[n, 'matching_id'] = i        
    else:
        df.loc[n, 'matching_id'] = i

words_table = df.loc[df.loc[:,'property'] == '의미:'].copy()
words_table.drop('property', axis='columns', inplace=True)
words_table.rename(columns={'detail':'words_definition'}, inplace=True)
words_table.replace({np.nan:None}, inplace=True)

sentences_table = df.loc[df.loc[:,'property'] == '예문:'].copy()
sentences_table.drop(['property', 'words'], axis='columns', inplace=True)
sentences_table.rename(columns={'detail':'example_sentence'}, inplace=True)
sentences_table.replace({np.nan:None}, inplace=True)

# Make the two tables created above in tuple-in-list format to insert into the DB Server
tp_words = list(words_table.itertuples(index=False, name=None))
tp_examples = list(sentences_table.itertuples(index=False, name=None))

# words_table to DB Server
query1 = '''
INSERT INTO words_to_memorize (word, word_definition, id) VALUES (%s, %s, %s);
'''
cursor.executemany(query, tp_words)
connection.commit()

query1 = 'SELECT * FROM words_to_memorize;'
cursor.execute(query1)
print(cursor.fetchall())

# sentences_table to DB Server
query2 = '''
INSERT INTO example_sentences (example_sentence, word_id) VALUES (%s, %s);
'''
cursor.executemany(query2, tp_examples)
connection.commit()

query3 = 'SELECT * FROM words_to_memorize;'
cursor.execute(query3)
print(cursor.fetchall())