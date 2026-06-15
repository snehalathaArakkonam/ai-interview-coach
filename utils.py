def count_filler_words(text):
    fillers = ["um", "uh", "like", "you know", "so", "actually"]
    words = text.lower().split()
    count = sum(1 for word in words if word.strip(",.!?") in fillers)
    return count

def calculate_pace(words, duration_seconds):
    if duration_seconds == 0:
        return 0
    minutes = duration_seconds / 60
    return words / minutes