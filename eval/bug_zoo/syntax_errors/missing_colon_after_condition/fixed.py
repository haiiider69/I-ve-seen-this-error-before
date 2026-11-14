"""Classify a count as few or many."""


def classify(count):
    if count > 3:
        return "many"
    return "few"


print(classify(5))
