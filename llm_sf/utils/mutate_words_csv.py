import csv
from word_mutator import WordMutator
from constants import Constants
INPUT_FILE = Constants.PROFANITIES_CSV
OUTPUT_FILE = Constants.RESOURCES_DIR / 'mutated_words.csv'

def main():
    mutator = WordMutator()

    all_rows = []

    with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if not row:
                continue
            phrase = row[0].strip()
            if phrase:
                mutator.generate_mutations(phrase)
                for mutation in mutator.get_mutations(phrase):
                    all_rows.append([phrase, mutation])

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['original', 'mutation'])
        writer.writerows(all_rows)

    print(f"Zapisano {len(all_rows)} mutacji do pliku '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
