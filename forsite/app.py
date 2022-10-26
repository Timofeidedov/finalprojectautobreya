import json

from flask import Flask
from flask import render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search')
def search():
  return render_template('search.html')
def results():
    input_string = request.args.get("input_str")
    print(input_string)
    search_result = search(input_string, 'corpus.json')
    return render_template("results.html", results=search_result)
def parse_a_query(query):
    parsed_query = []
    for big_part in query.split():
        new_item = {}
        for part in big_part.split('+'):
            if part[0] == '"' and part[-1] == '"':
                new_item['token'] = part[1:-1]
            elif part.isupper():
                new_item['pos'] = part
            else:
                new_item['lemma'] = part
        parsed_query.append(new_item)
    return parsed_query
def search(query, corpus):
    query = parse_a_query(query)
    for sent in corpus:
        if len(sent['token']) < len(query):
            continue
        for i in range(len(sent['token']) - len(query) + 1):
            for j in range(len(query)):
                for key in query[j]:
                    if query[j][key] != sent[key][i+j]:
                        break
                else:
                    continue
                break
            else:
                print(sent['sentence'], 'Источник: '+sent['source'], sep='\n', end='\n\n')
                break # каждое предложение из корпуса печатается 1 раз максимум
if __name__ == '__main__':
    app.run()
