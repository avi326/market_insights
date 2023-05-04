import re
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def has_any_kind_of_number(sentence):
    # Process the sentence using the spaCy model
    doc = nlp(sentence)

    # Check if any token in the sentence is a number or has a number-like entity
    for token in doc:
        if token.like_num or token.ent_type_ in ["CARDINAL", "ORDINAL", "QUANTITY", "MONEY", "PERCENT"]:
            return True

    # Return False if no numbers or number-like entities were found
    return False


def filter_sentences_with_numbers(text):
    # Split text into sentences
    sentences = text.split(".")

    # Filter out sentences with numbers
    filtered_sentences = [sentence for sentence in sentences if not has_any_kind_of_number(sentence)]

    return " ".join(filtered_sentences)


def get_first_1000_words(text):
    words = text.split()
    return ' '.join(words[:1000])


def filter_text_data(text_data, keys_to_keep):
    return [{k: v for k, v in data.items() if k in keys_to_keep} for data in text_data]


def filter_last_x_years_text_data(text_data, x_years):
    last_x_years_text_data = []
    for data in text_data:
        date = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
        x_years_ago = datetime.date.today() - datetime.timedelta(days=x_years * 365)
        if date > x_years_ago:
            last_x_years_text_data.append(data)
    return last_x_years_text_data


def truncate_text_data(text_data):
    for data in text_data:
        new_raw_text = utils.get_first_1000_words(data['raw_text'])
        data['raw_text'] = new_raw_text
    return text_data
