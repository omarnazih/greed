def telegram_html_escape(string: str):
    return string.replace("<", "&lt;") \
        .replace(">", "&gt;") \
        .replace("&", "&amp;") \
        .replace('"', "&quot;")



def get_value_inside_brackets(text: str):
    """This function get the values inside []"""
    start_index = text.find('[')
    end_index = text.find(']')
    if start_index != -1 and end_index != -1:
        return text[start_index+1:end_index].strip()
    return None



def get_values_around_dash(string):
    """Extracts the values before, after, and including the dash in a string.

    Args:
        string (str): The input string.

    Returns:
        Tuple[str, str]: A tuple containing the value before, after in the input string. Returns
                              empty strings for values that are not present.
    """
    index_of_dash = string.find("-")
    if index_of_dash == -1:
        return ("", "")
    else:
        before_dash = string[:index_of_dash]
        after_dash = string[index_of_dash + 1:]
        return (before_dash, after_dash)



def check_telegram_caption_length(text):
    """
    Checks if the length of the given text matches the Telegram character limit for a message caption.
    
    Args:
        text (str): The text to check.
    
    Returns:
        bool: True if the length of the text is within the Telegram limit, False otherwise.
    """
    TELEGRAM_CAPTION_LIMIT = 900
    return len(text) <= TELEGRAM_CAPTION_LIMIT    