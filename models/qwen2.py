import os

from openai import OpenAI

from needle_not_in_a_haystack import NeedleNotInAHaystack

DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY")

class Qwen272BNeedleNotInAHaystack(NeedleNotInAHaystack):
    model_name = 'Qwen/Qwen2-72B-Instruct'
    max_batch_size = 1024 * 1

    def llm(self, corpus: str, query: str) -> str:
        """
        Implement LLM invocation here.
        """
        client = OpenAI(api_key=DEEPINFRA_API_KEY, base_url='https://api.deepinfra.com/v1/openai')
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
    
class Qwen27BNeedleNotInAHaystack(Qwen272BNeedleNotInAHaystack):
    model_name = 'Qwen/Qwen2-7B-Instruct'
    max_batch_size = 1024