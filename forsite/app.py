import json
import re
from flask import Flask
from flask import render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search.html')
def search():
  return render_template('search.html')
@app.route('/results.html', methods=['get'])
def results():
    input_string = request.args.get("input_str")
    print(input_string)
    search_result = search2(input_string, 'corpus.json')
    print(search_result)
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
def search2(query, corpus):
    with open('corpus.json', 'r', encoding='utf-8') as f_corp:
        corpus = json.load(f_corp)
    replys = []
    num_matches = 0
    query = parse_a_query(query)

    if query == []:
        replys.append('Ошибка: пустой запрос.')
        return replys

    for sent in corpus:
        if len(sent['token']) < len(query):
            continue
        for i in range(len(sent['token']) - len(query) + 1):
            match = [] # чтобы печатать совпадение, опционально
            for j in range(len(query)):
                match.append(sent['token'][i+j]) # будут печататься токены, соответствующие запросу
                for key in query[j]:
                    if query[j][key] != sent[key][i+j]:
                        break
                else:
                    continue
                break
            else:
                replys.append('Совпадение: ' + ' '.join(match) +'. Предложение: '+ '\n' + sent['sentence'] + '\n' + 'Источник: ' + sent['source'] + '\n\n')
                num_matches += 1
                # break # каждое предложение из корпуса будет печататься 1 раз максимум (можно включить и убрать печать совпадений)

    if num_matches == 0:
        replys.append('По этому запросу ничего не найдено.')
    else:
        replys.append('Итого найдено ' + str(num_matches) + ' совпадений.')
    return replys


if __name__ == '__main__':
    app.run()