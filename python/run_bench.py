import pandas as pd
import json
import paperqa
import uuid
import datetime

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
        
        output.append({
            "question": question,
            "model": model,
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
        sources = [{"key": c[0], "text": c[1]} for c in answer.contexts]
        output.append({
            "question": q,
            "model": model,
            "date": date,
            "answer": answer.answer,
            "sources": sources
        })

    return output

def main():
    sheets_output = sheet_results()
    json.dump(sheets_output, open('other.json', 'w'), indent=2)
    # unique questions
    questions = list(set([q['question'] for q in sheets_output]))
    paperqa_output = paper_qa(questions)
    json.dump(paperqa_output, open('paperqa.json', 'w'), indent=2)


if __name__ == '__main__':
    main()