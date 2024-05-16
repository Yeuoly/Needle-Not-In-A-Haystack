import os
from openai import OpenAI

from needle_not_in_a_haystack import NeedleNotInAHaystack

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class GPT35NeedleNotInAHaystack(NeedleNotInAHaystack):
    model_name = 'gpt-3.5-turbo'
    max_batch_size = 1024

    def llm(self, corpus: str, query: str) -> str:
        """
        Implement LLM invocation here.
        """
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    'role': 'system',
                    'content': 'You have lots of number, and each of them has a unique answer. You need to find the answer of a number.\n'
                        'Below are the numbers and their answers:\n' + corpus
                },
                {
                    'role': 'user',
                    'content': query
                }
            ],
            stream=False,
            temperature=0
        )

        text = response.choices[0].message.content

        return text
    
    def check_answer(self, response: str, needle: str) -> bool:
        """
        Return True if the response contains the needle, False otherwise
        """
        response = response.lower()
        if 'not' in response or 'sorry' in response or 'don\'t' in response or 'haven\'t' in response:
            return False
        return True
    
class GPT4NeedleNotInAHaystack(GPT35NeedleNotInAHaystack):
    model_name = 'gpt-4'
    max_batch_size = 1024 / 2

class GPT4TurboNeedleNotInAHaystack(GPT35NeedleNotInAHaystack):
    model_name = 'gpt-4-turbo'
    max_batch_size = 1024 * 8

class GPT4oNeedleNotInAHaystack(GPT35NeedleNotInAHaystack):
    model_name = 'gpt-4o'
    max_batch_size = 1024 * 8
