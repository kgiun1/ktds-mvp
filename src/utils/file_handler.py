def read_uploaded_file(uploaded_file):
    """
    Reads the contents of an uploaded text file.

    Parameters:
    uploaded_file: The uploaded file object.

    Returns:
    str: The contents of the file as a string.
    """
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        return content
    return ""

def process_file_content(content):
    """
    Processes the content of the uploaded file for the chatbot.

    Parameters:
    content: The raw content of the file.

    Returns:
    list: A list of processed lines or tokens from the content.
    """
    lines = content.splitlines()
    processed_lines = [line.strip() for line in lines if line.strip()]
    return processed_lines