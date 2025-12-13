import re
import logging

# ---------------------- Logging Setup ----------------------
logging.basicConfig(
    filename="chat_log.txt",
    level=logging.INFO,
    format="USER: %(message)s"
)

# ---------------------- Knowledge Base ----------------------
knowledge_base = {
    r"(what is ai|define ai|meaning of ai)": 
        "AI (Artificial Intelligence) is the simulation of human intelligence in machines.",
    
    r"(what is machine learning|define machine learning|meaning of machine learning)":
        "Machine Learning is a subset of AI that allows systems to learn from data.",
    
    r"(what is deep learning|define deep learning)":
        "Deep Learning is a type of machine learning using neural networks with many layers.",
}

# ---------------------- Intent Rules ----------------------
intents = {
    r"(hi|hello|hey)": "Hello! How can I help you today?",
    r"(bye|goodbye|see you)": "Goodbye! Have a great day!",
    r"(help|assist|support)": "Sure! You can ask me about AI, ML, or general questions.",
    r"(how are you)": "I'm just a bot, but I'm doing great!",
}

# ---------------------- Chatbot Response ----------------------
def get_response(user_input):
    user_input = user_input.lower()

    # Check intents
    for pattern, response in intents.items():
        if re.search(pattern, user_input):
            return response

    # Check knowledge base
    for pattern, answer in knowledge_base.items():
        if re.search(pattern, user_input):
            return answer

    # Fallback
    return "I'm not sure about that. You can ask me about AI, machine learning, or deep learning!"

# ---------------------- Main Chat Loop ----------------------
def chat():
    print("Chatbot: Hello! I am your simple AI chatbot. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye! Conversation saved in chat_log.txt")
            break

        response = get_response(user_input)

        # log user message
        logging.info(user_input)

        print("Chatbot:", response)

# ---------------------- Run Chatbot ----------------------
if __name__ == "__main__":
    chat()
