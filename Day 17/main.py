import question_model
from data import question_data
from quiz_brain import QuizBrain

question_bank = []  # Create an empty list to store the questions
for question in question_data:
    question_text = question["text"]
    question_answer = question["answer"]
    new_question = question_model.Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()    # Ask the next question
    


