""" This is a very simple for a FAQ bot, that provides reponse and feed backs about the 
popular Japanese Manga, One Piece,

One Piece is a popular manga so this bot is designed to answer some of the FAQ

This code was modified from the preexisting faq_bot_skeleton provided by the course.

Ibrahim Ahmed, 000880591, Mohawk College, January 2024

-- reference:
    One Piece Manga
    https://onepiece.fandom.com/wiki/One_Piece
    Library of Ohara YouTube Channel
"""
import random
import re
# this is a function defined to load the contents of a file into an array
def load_file_into_array(file_path):
    """Load the contents of a file into an array.
    This function will load the content of the questions and answers registered by the domain"""
    with open(file_path, 'r') as file:
        _array = [line.strip() for line in file.readlines()]
    return _array

# this function is to load our questions and answers
def load_FAQ_data():
    """This method returns a list of questions and answers. The
    lists are parallel, meaning that intent n pairs with response n."""

    questions = load_file_into_array("questions.txt")

    answers = load_file_into_array("answers.txt")

    return questions, answers

def understand(utterance):
    """This method processes an utterance to determine which intent it
    matches. The index of the intent is returned, or -1 if no intent
    is found."""

    global intents # declare that we will use a global variable

    try:
        return intents.index(utterance)
    except ValueError:
        return -1

# this is a function that returns a random response to the user request if the intention is out of current scope
def unknow_intention_response():
    unknow_reponses = ["Sorry, I have not been trained to respond to that question  yet!", "Worororor!! I can not answer to that now", "Oops, I need more information if I'll be able to help... Ask something about one piece", "( ^ _ ^ ) I am sorry, I can't help provide a response to that!"]
    random_index = random.randint(0, len(unknow_reponses) - 1)
    return unknow_reponses[random_index]

# this is a function that returns a random response to the user request if the intention is hello or a phrase to start the chat
def hello_intention_response():
    hello_reponses = ["Hello. I am KingRahim. How can I help you", "Hey, my nakama. Let's chat about One Piece!", "(^-^)Hi, do you wanna hear more about One Piece", "Goodday my good person. How can I be of assistance today?"]
    random_index = random.randint(0, len(hello_reponses) - 1)
    return hello_reponses[random_index]


def generate(intent):
    """This function returns an appropriate response given a user's
    intent."""

    global responses # declare that we will use a global variable

    if intent == -1:
        return unknow_intention_response()

    return responses[intent]

## Load the questions and responses
intents, responses = load_FAQ_data()

## a list of possible end of conversion strings.. this list will be used to check intent from the user to end the chat
end_of_chat_intent = ["farewell", "bye", "chao", "quit", "end"]


## a list of possible words to start a conversion.. this list will be used to check intent from the user to start the chat
start_of_chat_intent = ["hello", "hi", "hey", "olla"]

# function to check if goodbye intent is found in user utterance
def goodbye_intention(intent):
    """Check if goodbye intent is found in user utterance."""
    for stm in end_of_chat_intent:
        if re.search(stm, intent):
            return True
    return False

# a function to help communicate the purpose of the bot to user is the utterance involves help
def help_info():
    return """This is a simple FAQ bot about One Piece...
You can ask questions like 
1. 'What is One Piece?
2. 'Who wrote One Piece?'
3. 'What is the name of the main character?' and we can pick up from there"""

# function to check if the user's intent is to start a conversion from the utterance
def start_chat_intention(intent):
    """this function is to confirm that there is intention to start
    the conversation by checking for an enity from the start_of_chat_intent list"""
    for stm in start_of_chat_intent:
        if re.match(stm, intent):
            return True
    return False

## Main Function
def main():
    """Implements a chat session in the shell."""
    print("Hello! I am KingRahim, Your One Piece Chat Bot.")
    print("You can ask me questions about 'One Piece'. When you're done talking, just say 'goodbye'.")
    print()
    utterance = ""
    while True:
        text = input(">>> ")
        utterance = text.lower()
        if utterance.endswith("?") or utterance.endswith(".") or utterance.endswith(" "):
            utterance = utterance[0:len(utterance)-1]
        
        if goodbye_intention(utterance):
            print("Goodbye!")
            break
        elif start_chat_intention(utterance):
            hi = hello_intention_response()
            print(hi)
        elif re.match(r'help', utterance):
            help_response = help_info()
            print(help_response)
        else:
            intent = understand(utterance)
            response = generate(intent)
            print(response)
        print()

    print("It was nice speaking to you..!")

## Run the chat code
# the if statement checks whether or not this module is being run
# as a standalone module. If it is beign imported, the if condition
# will be false and it will not run the chat method.
if __name__ == "__main__":
    main()