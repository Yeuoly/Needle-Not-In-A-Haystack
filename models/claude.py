import os
from needle_not_in_a_haystack import NeedleNotInAHaystack
from anthropic import Anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

class Claude2NeedleNotInAHaystack(NeedleNotInAHaystack):
    concurrence = 4
    num_tests = 10
    batch_size = 500
    model_name = 'claude-2.1'

    def llm(self, corpus: str, query: str) -> str:
        """
        Implement LLM invocation here.
        """
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=self.model_name,
            temperature=0,
            stream=False,
            system='You have lots of number, and each of them has a unique answer. You need to find the answer of a number.\n'
                'Below are the numbers and their answers:\n' + corpus,
            messages=[
                {
                    'role': 'user',
                    'content': query
                }
            ],
            max_tokens=100,
        )

        return response.content[0].text

    def check_answer(self, response: str, needle: str) -> bool:
        """
        Return True if the response contains the needle, False otherwise
        """
        if 'not' in response or 'sorry' in response or 'don\'t' in response or 'haven\'t' in response or 'no' in response:
            return False
        return True
    
class Claude3HaikuNeedleNotInAHaystack(Claude2NeedleNotInAHaystack):
    concurrence = 4
    num_tests = 20
    batch_size = 500
    model_name = 'claude-3-haiku-20240307'

class Claude3OpusNeedleNotInAHaystack(Claude2NeedleNotInAHaystack):
    concurrence = 4
    num_tests = 20
    batch_size = 500
    model_name = 'claude-3-opus-20240229'

class Claude3SonnetNeedleNotInAHaystack(Claude2NeedleNotInAHaystack):
    concurrence = 4
    num_tests = 20
    batch_size = 500
    model_name = 'claude-3-sonnet-20240229'
