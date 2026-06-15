import random

question_banks = {
    "DSA": [
        "Explain how a HashMap works internally in Python/Java.",
        "Write a function to detect a cycle in a linked list.",
        "Implement binary search on a sorted array.",
        # Add 50+ more questions here
    ],
    "Machine Learning": [
        "Explain the bias-variance tradeoff.",
        "What is overfitting and how do you prevent it?",
        # Add more
    ],
    "Web Development": [
        "Explain the difference between HTTP and HTTPS.",
        "What is CORS and how does it work?",
        # Add more
    ],
    "HR": [
        "Tell me about yourself.",
        "Why do you want to work here?",
        # Add more
    ]
}

def get_question(domain, difficulty):
    questions = question_banks.get(domain, question_banks["DSA"])
    return random.choice(questions)

def get_sample_answer(domain, question):
    # Placeholder sample answers
    return "This is a strong sample answer using STAR method with clear technical details..."