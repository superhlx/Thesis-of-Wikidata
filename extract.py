import json
import pyconll



with open('/home/heluxue/gf-wikidata-tools/conllu_data/POW/POW_en.conllu', 'r', encoding='utf-8') as f:
    data = json.load(f)

unparsed_set = set(
    entry["Eng"]["str"]
    for entry in data.values()
    if entry["Eng"]["lin"] == "variants {}"
)
conllu_file = "/home/heluxue/gf-wikidata-tools/extraction/out/terms_Eng.conllu"
output_file = "/home/heluxue/gf-wikidata-tools/extraction/out/unparsed_terms.conllu"

with open(conllu_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    keep = False  
    sentence_buffer = [] 
    newpar_buffer = []  

    for line in f_in:
        if line.startswith("# newpar"):

            newpar_buffer = [line]
            continue  
        
        elif line.startswith("# text ="):
            sentence_text = line.strip().split("= ", 1)[1]
            keep = sentence_text in unparsed_set  
        
        sentence_buffer.append(line)  
        
        if line.strip() == "":  
            if keep:
                if newpar_buffer:
                    f_out.writelines(newpar_buffer)
                    newpar_buffer = []   

                f_out.writelines(sentence_buffer)
                f_out.write("\n")  
            
            sentence_buffer = []
            keep = False

    if keep and sentence_buffer:
        f_out.writelines(sentence_buffer)

