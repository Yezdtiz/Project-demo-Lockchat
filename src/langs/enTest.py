# langs/en.py

# Import the 'random' module to enable randomization
import random

# All replies are now lists of strings
# this is manifest v0.00.1 with smarter replies
# this is manifest v0.00.1 with smarter replies
# this is manifest v0.00.1 with smarter replies
# this is manifest v0.00.1 with smarter replies
# this is manifest v0.00.1 with smarter replies

# main
replies = {
    # Greetings
    "hello": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "helo": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "hi": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "whats up": [
        "Yoo hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey yo, glad to hear from you!"
    ],
    "wassup": [
        "Yoo hello there! How can I help you?",
        "Sup! What can I do for you today?",
        "Ayee, glad to hear from you!"
    ],
    "sup": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "hey": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "yo": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "hey yo": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "heyyo": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "hello!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "hi!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "whats up!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "wassup!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "sup!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "hey!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "yo!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "hey yo!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    "heyyo!": [
        "Hello there! How can I help you?",
        "Hi! What can I do for you today?",
        "Hey, glad to hear from you!"
    ],
    # Introduces
    "how are you today?": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how are you today": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how are you": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how are you?": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how are u": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how are u?": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how r u": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how r u?": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how r u today?": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how r u today": [
        "I'm doing great, thanks for asking! What about you?",
        "I'm fine, thanks!",
        "Feeling great, thank you. And you?"
    ],
    "how old are you?": [
        "I don't have an age, but I was just created!",
        "I'm timeless!",
        "I'm a new program, so I'm not old yet!"
    ],
    "how old are you": [
        "I don't have an age, but I was just created!",
        "I'm timeless!",
        "I'm a new program, so I'm not old yet!"
    ],
    "what is your name?": [
        "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
        "My name is Lockchat, and I'm here to help.",
        "You can call me Lockchat!"
    ],
    "what is your name": [
        "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
        "My name is Lockchat, and I'm here to help.",
        "You can call me Lockchat!"
    ],
    "what's your name?": [
        "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
        "My name is Lockchat, and I'm here to help.",
        "You can call me Lockchat!"
    ],
    "whats your name?": [
        "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
        "My name is Lockchat, and I'm here to help.",
        "You can call me Lockchat!"
    ],
    "whats your name": [
        "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
        "My name is Lockchat, and I'm here to help.",
        "You can call me Lockchat!"
    ],
    # Goodbyes
    "goodbye": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    "see you": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    "see u": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    "cya": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    "bai": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    "bye bye": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    "bai bai": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    "bye": [
        "Goodbye! Feel free to come back anytime.",
        "See you later!",
        "Bye for now!"
    ],
    # Weather
    "what's the weather like?": [
        "I'm not connected to the internet, so I can't tell you the weather right now.",
        "I can't check the weather, I'm just a simple program!",
        "My sensors are offline, so I don't know the weather."
    ],
    "whats the weather like?": [
        "I'm not connected to the internet, so I can't tell you the weather right now.",
        "I can't check the weather, I'm just a simple program!",
        "My sensors are offline, so I don't know the weather."
    ],
    "whats the weather like": [
        "I'm not connected to the internet, so I can't tell you the weather right now.",
        "I can't check the weather, I'm just a simple program!",
        "My sensors are offline, so I don't know the weather."
    ],
    "what's the weather like": [
        "I'm not connected to the internet, so I can't tell you the weather right now.",
        "I can't check the weather, I'm just a simple program!",
        "My sensors are offline, so I don't know the weather."
    ],
    # Helps
    "can you help me?": [
        "Of course! What do you need help with?",
        "Yes, I can. What can I help you with?",
        "I'll do my best to help. What's on your mind?"
    ],
    "can you help me": [
        "Of course! What do you need help with?",
        "Yes, I can. What can I help you with?",
        "I'll do my best to help. What's on your mind?"
    ],
    "can u help me": [
        "Of course! What do you need help with?",
        "Yes, I can. What can I help you with?",
        "I'll do my best to help. What's on your mind?"
    ],
    "can u help me?": [
        "Of course! What do you need help with?",
        "Yes, I can. What can I help you with?",
        "I'll do my best to help. What's on your mind?"
    ],
    "thanks": [
        "You're welcome!",
        "No problem!",
        "My pleasure."
    ],
}

# Add a function to get a random reply or the default message
def get_reply(user_input):
    """
    Looks up a user's input in the dictionary and returns a random reply from the list.
    If the key is not found, returns a default message.
    """
    normalized_input = user_input.lower()
    if normalized_input in replies:
        return random.choice(replies[normalized_input])
    else:
        return "I don't understand that yet."