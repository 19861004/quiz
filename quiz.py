import json, colorama, string
from random import shuffle

correct = 0
total = 0

def validate(s: str) -> int:
    if s == 'exit':
        print_result()
    while s.strip() not in ['a', 'b', 'c', 'd']:
        s = input()
    return string.ascii_lowercase.index(s.strip())

def print_result() -> None:
    print()
    print(colorama.Style.BRIGHT + "Correctas: {} / Total: {}".format(correct, total))
    exit(0)

def main():
    global correct, total
    quiz = {}
    with open('quiz.json', 'r', encoding='utf-8') as f:
        quiz = json.load(f)

    correct = 0
    shuffle(quiz)
    for question in quiz:
        print(colorama.Style.BRIGHT + question['question'])

        answer = question['answers'][question['correct']]
        shuffle(question['answers'])
        valid = question['answers'].index(answer)
        for i, a in enumerate(question['answers']):
            print(string.ascii_lowercase[i] + '.', a)

        r = validate(input())
        if r == valid:
            print(colorama.Fore.GREEN + 'Correcto!')
            correct += 1
        else:
            print(colorama.Fore.RED + 'Incorrecto, la respuesta era "{}"'.format(question['answers'][valid]))

        total += 1
        print()

    print_result()

if __name__ == '__main__':
    colorama.init(autoreset=True)
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_result()