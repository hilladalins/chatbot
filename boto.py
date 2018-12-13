"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json

ANSWERS_DICT = {"color": "purple", "weather": "rainy", "city": "Berlin", "country": "Israel",
                "food": "meatballs"}
CURSES = ("arse", "ass", "asshole", "bastard", "bitch", "crap", "cunt", "damn", "fuck", "holy shit",
          "mother fucker", "nigga", "nigger", "shit", "whore")


def handle_input(input_text):
    if check_if_swear(input_text):
        return "Why like this?? Go wash your mouth with a soap"
    global first_answer
    if first_answer:
        first_answer = False
        input_words = input_text.split()
        return hello(input_words[-1])
    elif input_text.endswith('?'):
        return give_answer(input_text)


def check_if_swear(text):
    words = text.split()
    for word in words:
        if word in CURSES:
            return True
    return False


first_answer = True


def hello(name):
    return "Hi {}, nice to meet you".format(name)


def give_answer(question, answers=ANSWERS_DICT):
    question = question[:-1]  # remove the question mark
    words = question.split()
    for word in words:
        if word in answers:
            answer = answers[word]
            return answer
    return "I don't know"


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    bot_message = handle_input(user_message)
    return json.dumps({"animation": "inlove", "msg": bot_message})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
