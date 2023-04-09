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