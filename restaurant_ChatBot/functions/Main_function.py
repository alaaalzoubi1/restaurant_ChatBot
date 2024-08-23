import re
import fasttext
from Add_order import replace_with_food
import spacy
def preprocess(text):
    # Check if the input is a string
    if isinstance(text, str):
        # Remove special characters except alphanumeric and space
        text = re.sub(r'[^\w\s\']', ' ', text)
        # Replace multiple spaces or newlines with a single space
        text = re.sub(r'[ \n]+', ' ', text)
        return text.strip().lower()  # Strip leading/trailing whitespace and convert to lower case
    else:
        # Handle non-string inputs, here we simply return an empty string
        return ''
def lemmatize_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    lemmas_string = ' '.join(lemmas)
    print(lemmas_string)
    return lemmas_string
def main_function(message,user_id):
    preprocessed_message = preprocess(message)
    preprocessed_message = replace_with_food(preprocessed_message)
    preprocessed_message = lemmatize_text(preprocessed_message)
    model = fasttext.load_model("final_model.bin")
    predict = model.predict(preprocessed_message)
    predict = predict[0][0]
    print(predict)
    response = ""
    if predict == "__label__welcome":
        import welcome_response as we
        response = we.get_random_phrase(user_id)
    elif predict == "__label__Review":
        from Reviewing import review
        response = review(message,user_id)
    elif predict == "__label__add_order":
        from Add_order import add_order
        response = add_order(message,user_id)
    elif predict == "__label__edit_order":
        from Edit_order import edit_order
        response = edit_order(message,user_id)
    elif predict == "__label__menu_request":
        from request_menu import get_menu_names
        response = get_menu_names()
    elif predict == "__label__complete_order":
        from Order_complete import order_complete
        response = order_complete(message,user_id)
    elif predict == "__label__new_order":
        from New_order import new_order
        response = new_order(message, user_id)
    elif predict == "__label__Edit_Reservation":
        from Edit_reservation import edit_reservation
        response = edit_reservation(message,user_id)
    elif predict == "__label__cancel_reservation":
        from cancel_reservation import cancel_reservation
        response = cancel_reservation(message, user_id)
    elif predict == "__label__add_reservation":
        from Add_reservation import add_reservation
        response = add_reservation(message, user_id)
    elif predict == "__label__check_order":
        from Check_order import check_order
        response = check_order(message,user_id)
    elif predict == "__label__remove_order":
        from Remove_order import remove_order
        response = remove_order(message,user_id)
    else:
        from Fallback import fallback
        response = fallback()
    return response
