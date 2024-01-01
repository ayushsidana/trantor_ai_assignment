import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_streamlined_stored_answer(answer):
    """
    Generator function that breaks down the given 'answer' string into chunks of 10 characters each.
    
    Args:
    - answer (str): The input string that needs to be segmented.
    
    Yields:
    - str: Chunks of 10 characters from the input 'answer' string.
    """
    for chunk in [answer[i:i + 10] for i in range(0, len(answer), 10)]:
        yield chunk
