from abc import ABC, abstractmethod
from threading import Lock, Thread
from typing import Generator
from random import randint
from tqdm import tqdm

from utils import generate_sentence

def get_green_text(text: str) -> str:
    """
    Get red colored text

    :param text: text to color

    :return: colored text
    """
    return f"\033[92m{text}\033[00m"

class NeedleNotInAHaystack(ABC):
    model_name = "NoneModel"
    concurrence = 10
    num_tests = 50
    batch_size = 500

    @abstractmethod
    def llm(self, corpus: str, query: str) -> str:
        """
        Implement LLM invocation here.
        """

    @abstractmethod
    def check_answer(self, response: str, needle: str) -> bool:
        """
        Return True if the response contains the needle, False otherwise
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

    def test(self) -> None:
        """
        Run tests, yield current test result
        """
        sets = self.generate_test_sets(self.batch_size, self.num_tests)

        result = {
            'right': 0,
            'wrong': 0,
            'index': 0
        }

        with tqdm(total=len(sets)) as pbar:
            def test(sets: list[tuple[str, str, str]], lock: Lock, result: dict[str, int], pbar: tqdm):
                while True:
                    with lock:
                        index = result['index']
                        if index >= len(sets):
                            break
                        result['index'] += 1

                    query, haystack, needle = sets[index]
                    response = self.llm(haystack, query)
                    if not self.check_answer(response, needle):
                        with lock:
                            result['right'] += 1
                    else:
                        with lock:
                            result['wrong'] += 1
                    # set description
                    pbar.set_description(f"{self.model_name} accuracy: \033[92m%{(result['right'] / (result['right'] + result['wrong']) * 100):.0f}\033[00m")
                    pbar.update(1)
                    
            threads = []
            lock = Lock()

            for _ in range(0, min(self.concurrence, len(sets))):
                threads.append(Thread(target=test, args=(sets, lock, result, pbar)))
                threads[-1].start()

            for thread in threads:
                thread.join()
