from abc import ABC, abstractmethod
from typing import Generator
from random import randint
from utils import generate_sentence

class NeedleNotInAHaystack(ABC):
    @abstractmethod
    def llm(self, corpus: str, query: str) -> str:
        """
        Implement LLM invocation here.
        """

    def generate_random_string(self, length: int) -> str:
        """
        Generate a random string of given length

        :param length: length of the string

        :return: random string
        """
        return ''.join([chr(randint(0, 25) + 65) for _ in range(length)])

    def generate_test_sets(self, batch: int, nums: int) -> list[tuple[str, str, str, str]]:
        """
        Generate test sets with random data

        :param batch: how many needles in single test set
        :param nums: how many test sets to generate

        :return: list of test sets
            (query, haystack, needle)
        """
        result = []
        for _ in range(nums):
            not_to_generate_needle = randint(0, 100000000)
            query = f"give me the answer of {not_to_generate_needle}"
            haystack = ""
            for _ in range(batch):
                needle = randint(0, 100000000)
                while needle == not_to_generate_needle:
                    needle = randint(0, 100000000)
                haystack += f"\n## Answer of {needle}"
                haystack += f"\n{generate_sentence()}"

            result.append((query, haystack, not_to_generate_needle))

        return result

    def test(self) -> Generator[float, None, None]:
        """
        Run tests, yield current test result
        """
        sets = self.generate_test_sets(300, 10)
        
        for query, haystack, needle in sets:
            result = self.llm(haystack, query)

            print(result)