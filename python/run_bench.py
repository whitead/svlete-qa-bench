import pandas as pd
import json
import paperqa
import uuid
import datetime
import sys


names = ['paperqa', 'bing', 'perplexity', 'scite', 'chatsonic']


def sheet_results():
    SPREADSHEET_ID = '1MuQimMdQNXHKmLWVzhaQzFxhTTGDTopUa_325LIt7t8'
    SHEET_NAME = 'Answers'

    url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(url)

    output = []
    for _, row in df.iterrows():
        question = row['Question']
        model = row['Service']
        date = row['Date']
        answer = row['Answer']
        sources = []
        for i in range(1, 11):
            citation_text = f'Citation #{i}'
            if pd.notnull(row[citation_text]):
                sources.append({"key": str(i), "text": row[citation_text]})
        name = next((n for n in names if n in model.casefold()), None)
        if name is None:
            raise ValueError(f'Unknown model: {model}')
        if name == 'paperqa':
            name = f'{name}-{paperqa.__version__}'
        output.append({
            "question": question,
            "model": name,
            "date": date,
            "answer": answer,
            "sources": sources
        })

    return output


def paper_qa(questions):

    output = []
    model = f'paperqa-{paperqa.__version__}'
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    for q in questions:
        session_id = str(uuid.uuid4())
        docs = paperqa.Docs(name=session_id)
        answer = paperqa.run_agent(docs, q)
        sources = [{"key": c.key, "text": c.citation} for c in answer.contexts]
        yield dict({
            "question": q,
            "model": model,
            "date": date,
            "answer": answer.answer,
            "sources": sources
        })

    return output


def merge_results(new_results):
    with open('../src/data.js') as json_file:
        json_file.readline()
        old = json.load(json_file)
    # revise old names to match new names
    for o in old:
        if not 'paperqa' in o['model']:
            name = next((n for n in names if n in o['model'].casefold()), None)
            if name is None:
                raise ValueError(f'Unknown model: {o["model"]}')
            o['model'] = name
    old.extend(new_results)
    keys = set()
    to_delete = []
    for o in old:
        key = (o['question'], o['model'], o['date'])
        if key in keys:
            to_delete.append(o)
        keys.add(key)
    for o in to_delete:
        old.remove(o)
    return old


def main():
    sheets_output = sheet_results()
    merged_results = merge_results(sheets_output)
    json.dump(merged_results, open('other.json', 'w'), indent=2)
    # unique questions
    questions = list(set([q['question'] for q in sheets_output]))
    # if there are sys args, filter questions to those with
    # the words in them
    if len(sys.argv) > 1:
        questions = [q for q in questions if all(
            [w in q.casefold() for w in sys.argv[1:]])]
    return
    with open('paperqa.json', 'w') as f:
        for p in paper_qa(questions):
            json.dump(p, f, indent=2)


if __name__ == '__main__':
    main()
