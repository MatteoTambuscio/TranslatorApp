"""import stanza

# processors={"pos":"combined"}
#stanza.download('en', processors=["pos", "tokenize", "mwt"], model_dir='https://github.com/MatteoTambuscio/TranslatorApp/tree/main/resources_en/') #processors={"tokenize":"mwt"}, model_dir='resources_en/')
#stanza.download('it', processors=["pos", "tokenize", "mwt"], model_dir='https://github.com/MatteoTambuscio/TranslatorApp/tree/main/resources_it/') #processors="tokenize", package="ewt", model_dir='resources_it/')
nlp = { "IT": stanza.Pipeline('it', model_dir="https://github.com/MatteoTambuscio/TranslatorApp/tree/main/resources_it", processors='pos,tokenize,mwt', download_method=None),
        "EN": stanza.Pipeline('en', model_dir="https://github.com/MatteoTambuscio/TranslatorApp/tree/main/resources_en", processors='pos,tokenize,mwt', download_method=None) }

def true_text(text, target_len):

    doc = nlp[target_len](text)
    clean_text = []
    for sentence in doc.sentences:
        PROPN = []

        for w in sentence.words:
            if w.upos in ["PROPN"]:
                PROPN.append(w.text.capitalize())

        true_sentence = sentence.text.capitalize()
        for word in PROPN:
            true_sentence = true_sentence.replace(word.lower(), word)

        clean_text.append(true_sentence)
    output = " ".join(clean_text)

    return output
"""

