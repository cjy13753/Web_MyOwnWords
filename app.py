from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import mysql.connector



# Rendering HTML template
@app.route('/')
def home():
    return render_template('index.html')

# API that fetches word and example sentence from DB
@app.route('/fetch_word', methods=['GET'])
def fetch_word():
    ## Connect to DB
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="test_yourownwords"
    )
    mycursor = mydb.cursor()
    
    ## fetch word
    query_fetch_word = '''
        SELECT id, word, word_definition, counts_of_memory FROM words_to_memorize
            ORDER BY counts_of_memory ASC, word ASC
            LIMIT 1
    '''
    mycursor.execute(query_fetch_word)
    word = mycursor.fetchall()
    
    ## fetch example sentence
    word_id = (word[0][0],)
    query_fetch_examplesentence = '''
        SELECT example_sentence, context, web_link FROM example_sentences
            WHERE word_id = %s
            ORDER BY gen_time ASC
    '''
    mycursor.execute(query_fetch_examplesentence, word_id)
    example_sentence = mycursor.fetchall()

    return jsonify({'result':'success', 'word': word, 'example_sentence': example_sentence})



# API that inserts new example sentence to DB from browser
@app.route('/add_newsentence', methods=['POST'])
def add_newsentence():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="test_yourownwords"
    )
    mycursor = mydb.cursor()
    
    # Fetch information from the browser
    word_id_receive = request.form['word_id_give']
    example_sentence_receive = request.form['example_sentence_give']
    context_receive = request.form['context_give']
    web_link_receive = request.form['web_link_give']

    # Insert into DB
    query_insert_examplesentence1 = '''
        INSERT INTO example_sentences (word_id, example_sentence, context, web_link) VALUES (%s, %s, %s, %s);
    '''
    param1 = (word_id_receive, example_sentence_receive, context_receive, web_link_receive)
    mycursor.execute(query_insert_examplesentence1, param1)
    mydb.commit()
    
    query_insert_examplesentence2 = '''
        UPDATE words_to_memorize SET counts_of_memory = counts_of_memory + 1 WHERE id = %s;
    '''
    param2 = (word_id_receive,)
    mycursor.execute(query_insert_examplesentence2, param2)
    mydb.commit()

    return jsonify({'result': 'success', 'msg': 'Successful!'})






if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)