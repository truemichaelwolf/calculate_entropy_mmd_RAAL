import spacy
import math, os
from collections import Counter, defaultdict
import pandas as pd

def calculate_entropy_spacy(doc):
    # Count the frequency of each token
    frequencies = Counter([token.text for token in doc if not token.is_punct and not token.is_space])
    total_tokens = sum(frequencies.values())

    # Calculate the entropy
    entropy = -sum((freq / total_tokens) * math.log2(freq / total_tokens) 
                   for freq in frequencies.values())

    return entropy

def calculate_corrected_entropy(doc):
    # This function uses Millar-Madow correction to calculate the entropy
    # which is number of types minus 1 divided by two times of number of tokens
    original_entropy = calculate_entropy_spacy(doc)
    num_type = len(set([token.text for token in doc if not token.is_punct and not token.is_space]))
    num_tokens = sum(1 for token in doc if not token.is_punct and not token.is_space)
    new_entropy = original_entropy + ((num_type - 1) / (2 * num_tokens))
    return new_entropy

def calculate_MM_estimate(doc):
    # This function uses Millar-Madow correction to calculate the entropy
    # which is number of types minus 1 divided by two times of number of tokens
    num_type = len(set([token.text for token in doc if not token.is_punct and not token.is_space]))
    num_tokens = sum(1 for token in doc if not token.is_punct and not token.is_space)
    MM_estimate = ((num_type - 1) / (2 * num_tokens))
    return MM_estimate

def mean_dependency_distance(doc):
    total_distance = 0
    total_tokens = 0

    for token in doc:
        if not token.is_punct and not token.is_space:
            # Distance between a token and its head
            distance = abs(token.i - token.head.i)
            total_distance += distance
            total_tokens += 1

    return total_distance / total_tokens if total_tokens > 0 else 0

if __name__ == '__main__':
    base_dir = r"Corpora\RAAL"
    # create a dictionary of the paths to the files
    file_paths = {file: os.path.join(base_dir, file) for file in os.listdir(base_dir) if file.endswith(".txt")}

# Load SpaCy model
nlp = spacy.load('en_core_web_md')
results = defaultdict(list)
for k, v in file_paths.items():
    print(k)
    results['file'].append(k)
    results['discipline'].append(k[0])
    results['time'].append(k[1])
    results['paradigm'].append(k[2])
    with open(v, 'r', encoding='utf-8') as f:
        text = f.read()
    doc = nlp(text)
    entropy = calculate_entropy_spacy(doc)
    corrected_entropy = calculate_corrected_entropy(doc)
    results['entropy'].append(entropy)
    results['corrected_entropy'].append(corrected_entropy)
    mean_distance = mean_dependency_distance(doc)
    results['mean_distance'].append(mean_distance)

    df = pd.DataFrame(results)
    df.to_excel('AL_corrected_entropy_mdd.xlsx', index=False)
