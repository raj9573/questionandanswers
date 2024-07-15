
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not current_question_id:
        return False, "No current question found."

    # Assuming session is a Django session object
    answers = session.get("answers", {})

    # Store the answer for the current question
    answers[current_question_id] = answer
    session["answers"] = answers  # Update the answers in session

    return True, ""




def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        # If there's no current question ID, return the first question
        first_question = PYTHON_QUESTION_LIST[0]
        return first_question['question_text'], 0
    
    # Find the index of the current question_id
    current_index = current_question_id + 1
    
    if current_index < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[current_index]
        return next_question['question_text'], current_index
    else:
        return None, None  # Return None if no next question found


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get("answers", {})

    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for idx, question in enumerate(PYTHON_QUESTION_LIST):
        question_id = idx  # Assuming question_id is the index in the list
        if str(question_id) in answers:
            user_answer = answers[str(question_id)]
            if user_answer == question['answer']:
                correct_answers += 1

    score = (correct_answers / total_questions) * 100  # Calculate score percentage

    return f"You answered {correct_answers} out of {total_questions} questions correctly. Your score is {score:.2f}%."
