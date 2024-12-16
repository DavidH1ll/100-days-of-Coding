import random


# Word bank
words = ['python', 'programming', 'computer', 'algorithm', 'database', 
         'network', 'software', 'developer', 'internet', 'javascript']

chosen_word = random.choice(words)
placeholder = ""



for _ in range(len(chosen_word)):
    placeholder += "_"


print(chosen_word)
print(placeholder)


guess = input("Guess a letter: ").lower()
print(guess)


display = ""
for letter in chosen_word:
    if letter == guess:
        display += letter 
    else:
        display += "_"


print(display)