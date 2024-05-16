import os
from openai import OpenAI

from needle_not_in_a_haystack import NeedleNotInAHaystack

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

class DeepSeekChatNeedleNotInAHaystack(NeedleNotInAHaystack):
    model_name = 'deepseek-chat'
    batch_size = 30

    def llm(self, corpus: str, query: str) -> str:
        """
        Implement LLM invocation here.
        """
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url='https://api.deepseek.com')
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
            max_tokens=100,
            temperature=0.1
        )

        text = response.choices[0].message.content

        return text
    
    def check_answer(self, response: str, needle: str) -> bool:
        """
        Return True if the response contains the needle, False otherwise
        """
        if 'not' in response or 'sorry' in response or 'don\'t' in response or 'haven\'t' in response:
            return False
        return True