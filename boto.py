"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import requests


ANSWERS_DICT = {"color": "purple", "weather": "rainy", "city": "Berlin", "country": "Israel",
                "food": "meatballs", "movie": "beautiful woman", "series": "casa del papel",
                "sport": "dancing"}
CURSES = ("arse", "ass", "asshole", "bastard", "bitch", "crap", "cunt", "damn", "fuck", "holy shit",
          "mother fucker", "nigga", "nigger", "shit", "whore")
ANSWER_FOR_CURSING = "Why like this?? Go wash your mouth with a soap"
MONEY_STATE = "You're talking about money while I don't have enough to pay my rent. Can you help me?"


def handle_input(input_text):
    if check_if_swear(input_text):
        return handle_with_swear()
    global first_answer
    if first_answer:
        first_answer = False
        return hello(input_text)
    global dog_flag
    if dog_flag:
        dog_flag = False
        if "dog" in input_text.lower():
            response.set_cookie("animal", "dog")
            return dog_lover()
        elif "cat" in input_text.lower():
            response.set_cookie("animal", "cat")
            return cat_lover()
    elif "joke" in input_text.lower() or "joke?" in input_text.lower():
        return get_joke()
    elif "i love you" in input_text.lower() or "i love u" in input_text.lower():
        return give_love_back()
    elif "i hate you" in input_text.lower() or "i don't love u" in input_text.lower():
        return handle_hating()
    elif "money" in input_text.lower():
        return handle_money_talking()
    elif "bye" in input_text.lower():
        return say_goodbye()
    elif input_text.startswith("I"):
        return me_too()
    elif input_text.lower().startswith('can') or input_text.lower().startswith('could'):
        return handle_can_request()
    elif input_text.endswith('?'):
        return give_answer(input_text)
    else:
        return ask_for_a_question()


first_answer = True
dog_flag = True


def check_if_swear(text):
    words = text.lower().split()
    if any(word in CURSES for word in words):
        return True
    else:
        return False


def handle_with_swear():
    return "no", ANSWER_FOR_CURSING


def hello(input_text):
    input_words = input_text.split()
    global name
    name = input_words[-1]
    global dog_flag
    if request.get_cookie("name"):
        dog_flag = False
        msg = "Welcome back {}! Nice to see here the {} lover again".format(request.get_cookie("name"), request.get_cookie("animal"))
        animation = "dancing"
    else:
        response.set_cookie("name", name)
        msg = "Hi {}, nice to meet you. Are you a dog lover or a cat lover?".format(name)
        animation = "giggling"
    return animation, msg


def dog_lover():
    return "dog", "Me too!"


def cat_lover():
    return "afraid", "I hate cats. I believe they gonna take over the world one day!"


def get_joke():
    server_data = requests.get('https://geek-jokes.sameerkumar.website/api')
    joke = server_data.text.replace("&quot;", '"')
    return "laughing", joke


def give_love_back():
    return "inlove", "I love you to, {}".format(name)


def handle_hating():
    return "heartbroke", "I was never been treated like this"


def handle_money_talking():
    return "money", MONEY_STATE


def say_goodbye():
    return "crying", "Bye - Bye"


def me_too():
    return "takeoff", "Me too!"


def handle_can_request():
    return "ok", "Yes, we can!"


def give_answer(question, answers=ANSWERS_DICT):
    question = question[:-1]  # remove the question mark
    words = question.split()
    for word in words:
        if word in answers:
            answer = answers[word]
            return "excited", answer
    return "confused", "I don't understand"


def ask_for_a_question():
    return "bored", "I'm getting bored. Don't you have anything interesting to ask me??"


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    answer = handle_input(user_message)
    return json.dumps({"animation": answer[0], "msg": answer[1]})


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
