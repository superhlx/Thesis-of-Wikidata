import pyconll
from collections import Counter


conllu_file = "/home/heluxue/gf-wikidata-tools/conllu_data/university/uni_en.conllu"
conllu_data = pyconll.load_from_file(conllu_file)


word_counts = Counter()

for sentence in conllu_data:
    for token in sentence:
        word_counts[token.form.lower()] += 1  

print("the 50st most common words in unparsed sentences:")
for word, count in word_counts.most_common(50):
    print(f"{word}: {count}")


upos_counts = Counter()

for sentence in conllu_data:
    for token in sentence:
        upos_counts[token.upos] += 1  


print("part of speech statistics for unparsed sentences:")
for upos, count in upos_counts.items():
    print(f"{upos}: {count}")

failed_root_sentences = 0
unknown_pos_tokens = 0
unknown_deprel_tokens = 0

for sentence in conllu_data:
    has_root = any(token.deprel == "root" for token in sentence)
    if not has_root:
        failed_root_sentences += 1

    for token in sentence:
        if token.upos == "X":  
            unknown_pos_tokens += 1
        if token.deprel == "DEP":  
            unknown_deprel_tokens += 1

print(f"sentences don't have a root: {failed_root_sentences}")
print(f"number of unknown_pos_tokens: {unknown_pos_tokens}")
print(f"number of unknown_deprel_tokens : {unknown_deprel_tokens}")


from collections import defaultdict

bigram_counts = defaultdict(int)

for sentence in conllu_data:
    tokens = [token.form.lower() for token in sentence]
    for i in range(len(tokens) - 1):
        bigram = f"{tokens[i]} {tokens[i+1]}"
        bigram_counts[bigram] += 1

print("Most common phrases in unparsed sentences (top 30):")
for bigram, count in sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)[:30]:
    print(f"{bigram}: {count}")