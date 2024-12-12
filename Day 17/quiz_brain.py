import os

class QuizBrain:
    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        current_question = self.question_list[self.question_number]
        self.question_number += 1
        while True:
            user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ")
            if user_answer.lower() in ['true', 'false']:
                break
            print("Please answer with True or False")
        self.check_answer(user_answer, current_question.answer)
        self.display_score()
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_answer(self, user_answer: str, correct_answer: str) -> None:
        # Convert answers to strings and lowercase for comparison
        user_answer = str(user_answer).lower()
        correct_answer = str(correct_answer).lower()
        
        if user_answer == correct_answer:
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong.")
        print(f"The correct answer was: {correct_answer.capitalize()}")
        print(f"Your current score is: {self.score}/{self.question_number}\n")

    def display_score(self):
        print(f"Your current score is: {self.score}/{self.question_number}")