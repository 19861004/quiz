import requests, bs4, time, json, re

def main():
    j = []

    session = requests.Session()
    session.headers.update({
        'Cookie': r'' # poned aquí las cookies
    })

    r = session.get('https://campus.uax.es/moodle/course/view.php?id=4914') # aquí la id del módulo
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    quiz = [x['href'] for x in soup.find_all('a', href=True) if 'quiz' in x['href']]

    attempts = []
    for q in quiz:
        r = session.get(q)
        s = bs4.BeautifulSoup(r.text, 'html.parser')
        a = [x['href'] for x in s.find_all('a', href=True) if 'review.php?attempt' in x['href']]

        attempts.extend(a)
        time.sleep(1)

    i = 0
    for a in attempts:
        r = session.get(a)
        s = bs4.BeautifulSoup(r.text, 'html.parser')

        for qb in s.find_all('div', id=re.compile('^question-')):
            q = qb.find('div', {'class': 'qtext'}).text
            an = [x.text[3:] for x in qb.find_all('div', {'data-region': 'answer-label'})]
            ra = qb.find('div', {'class': 'rightanswer'}).text[26:]
            rai = an.index(ra)

            j.append({
                'id': i,
                'question': q,
                'answers': an,
                'correct': rai
            })

            i += 1

        time.sleep(1)

    with open('quiz.json', 'w', encoding='utf-8') as f:
        json.dump(j, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()