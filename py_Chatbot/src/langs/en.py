# langs/en.py
# Use a dictionary to store user input to bot replies.
# All keys must be in lowercase.
replies = {
    # Greetings
    "hello": "Hello there! How can I help you?",
    "helo": "Hello there! How can I help you?",
    "hi": "Hello there! How can I help you?",
    "whats up": "Hello there! How can I help you?",
    "wassup": "Hello there! How can I help you?",
    "sup": "Hello there! How can I help you?",
    "hey": "Hello there! How can I help you?",
    "yo": "Hello there! How can I help you?",
    "hey yo": "Hello there! How can I help you?",
    "heyyo": "Hello there! How can I help you?",
    "hello!": "Hello there! How can I help you?",
    "hi!": "Hello there! How can I help you?",
    "whats up!": "Hello there! How can I help you?",
    "wassup!": "Hello there! How can I help you?",
    "sup!": "Hello there! How can I help you?",
    "hey!": "Hello there! How can I help you?",
    "yo!": "Hello there! How can I help you?",
    "hey yo!": "Hello there! How can I help you?",
    "heyyo!": "Hello there! How can I help you?",
    # Introduces
    "how are you today?": "I'm doing great, thanks for asking! What about you?",
    "how are you today": "I'm doing great, thanks for asking! What about you?",
    "how are you": "I'm doing great, thanks for asking! What about you?",
    "how are you?": "I'm doing great, thanks for asking! What about you?",
    "how are u": "I'm doing great, thanks for asking! What about you?",
    "how are u?": "I'm doing great, thanks for asking! What about you?",
    "how r u": "I'm doing great, thanks for asking! What about you?",
    "how r u?": "I'm doing great, thanks for asking! What about you?",
    "how r u today?": "I'm doing great, thanks for asking! What about you?",
    "how r u today": "I'm doing great, thanks for asking! What about you?",
    "how old are you?": "I don't have an age, but I was just created!",
    "how old are you": "I don't have an age, but I was just created!",
    "what is your name?": "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
    "what is your name": "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
    "what's your name?": "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
    "whats your name?": "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
    "whats your name": "I'm a chatbot named Lockchat. It's a pleasure to meet you.",
    # Goodbyes
    "goodbye": "Goodbye! Feel free to come back anytime.",
    "see you": "Goodbye! Feel free to come back anytime.",
    "see u": "Goodbye! Feel free to come back anytime.",
    "cya": "Goodbye! Feel free to come back anytime.",
    "bai": "Goodbye! Feel free to come back anytime.",
    "bye bye": "Goodbye! Feel free to come back anytime.",
    "bai bai": "Goodbye! Feel free to come back anytime.",
    "bye": "Goodbye! Feel free to come back anytime.",
    # Weather
    "what's the weather like?": "I'm not connected to the internet, so I can't tell you the weather right now.",
    "whats the weather like?": "I'm not connected to the internet, so I can't tell you the weather right now.",
    "whats the weather like": "I'm not connected to the internet, so I can't tell you the weather right now.",
    "what's the weather like": "I'm not connected to the internet, so I can't tell you the weather right now.",
    # Helps
    "can you help me?": "Of course! What do you need help with?",
    "can you help me": "Of course! What do you need help with?",
    "can u help me": "Of course! What do you need help with?",
    "can u help me?": "Of course! What do you need help with?",
    "thanks": "You're welcome!",
}

# single reply
def get_reply(user_input):
    """
    Looks up a user's input in the dictionary and returns a single reply.
    If the key is not found, returns a default message.
    """
    normalized_input = user_input.lower()
    return replies.get(normalized_input, "I don't understand that yet.")