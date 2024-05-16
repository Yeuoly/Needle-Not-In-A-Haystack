import os

from needle_not_in_a_haystack import NeedleNotInAHaystack
from openai import OpenAI
from dotenv import load_dotenv

class GPT4onNeedleNotInAHaystack(NeedleNotInAHaystack):
    def llm(self, corpus: str, query: str) -> str:
        """
        Implement LLM invocation here.
        """
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o",
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
            stream=False
        )

        text = response.choices[0].message.content

        return text

if __name__ == "__main__":
    load_dotenv()

    nnh = GPT4onNeedleNotInAHaystack()
    nnh.test()