import random
import string
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import current_thread

random.seed(0)
dna = [[''.join((random.choice('ATGC') for j in range(1000)))] for i in range(100)]


def findDNA(dna_sample):
    text = dna_sample.pop()
    result = text.find('ATGC')
    if result == -1:
        return "ATGC not found in " + text
    else:
        return "ATGC is found in " + text


def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(findDNA, dna)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
