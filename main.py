import streamlit as st
import sentencepiece as spm
import ctranslate2
from nltk import sent_tokenize
#from trueCaser import true_text
#import deepl
#translator_deep = deepl.Translator("074d5d22-b571-4e24-61af-361aacd3234f:fx")
#import nltk
#nltk.download('punkt')

if 'sen' not in st.session_state:
    st.session_state['sen'] = ""

if 'cic' not in st.session_state:
    st.session_state['cic'] = ""


def _max_width_(prcnt_width:int = 80):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f""" 
                <style> 
                .reportview-container .main .block-container{{{max_width_str}}}
                </style>    
                """,
                unsafe_allow_html=True,
    )


def clear_text():
    st.session_state['user_input'] = ""

def call_2():
    st.session_state['sen'] = st.session_state['cic']


def translate(source, translator, sp_source_model, sp_target_model):
    """Use CTranslate model to translate a sentence

    Args:
        source (str): Source sentences to translate
        translator (object): Object of Translator, with the CTranslate2 model
        sp_source_model (object): Object of SentencePieceProcessor, with the SentencePiece source model
        sp_target_model (object): Object of SentencePieceProcessor, with the SentencePiece target model
    Returns:
        Translation of the source text"""

    source_sentences = sent_tokenize(source)
    source_tokenized = sp_source_model.encode(source_sentences, out_type=str)
    translations = translator.translate_batch(source_tokenized, beam_size=5)
    translations = [translation[0]["tokens"] for translation in translations]
    translations_detokenized = sp_target_model.decode(translations)
    translation = " ".join(translations_detokenized)

    return translation



@st.cache(allow_output_mutation=True)
def load_models(source_len, target_len, domain):
    ct_model_path = "model/"+domain+"/"+source_len+"_"+target_len
    sp_source_model_path = "model/vocab_model/"+source_len+".model"
    sp_target_model_path = "model/vocab_model/"+target_len+".model"

    translator = ctranslate2.Translator(ct_model_path)
    sp_source_model = spm.SentencePieceProcessor(sp_source_model_path)
    sp_target_model = spm.SentencePieceProcessor(sp_target_model_path)

    return translator, sp_source_model, sp_target_model


_max_width_()
# Title for the page and icon
#st.set_page_config(page_title="NMT")
# Header
st.title("Translator")

# Form to add your items
#with st.form("my_form"):
left_column, c_column, right_column = st.columns(3)
# Dropdown menu to select source and target language
source_len = left_column.selectbox(
        "Source language",
        ("EN", "IT"))

target_len = c_column.selectbox(
        "target language",
        ("IT", "EN"))

# select the domain of the text
domain = right_column.selectbox(
        "Select the model to use",
        ("general", "marketing", "Deepl"))

left_column2, right_column2 = st.columns(2)
# Textarea to type the source text.
user_input = left_column2.text_area("Source Text", height=200, max_chars=5000, key="user_input")

# Load models
if source_len != target_len:

 # translator, sp_source_model, sp_target_model = load_models(source_len, target_len, domain)

 # Translate with CTranslate2 model
# if domain != "Deepl":
  translator, sp_source_model, sp_target_model = load_models(source_len, target_len, domain)
  translation = translate(user_input.lower(), translator, sp_source_model, sp_target_model)
# else:
#  translation = translator_deep.translate_text(user_input.lower(), target_len).text #, from_lang=source_len)

# Create a button
left_column3, central_column3, right_column3 = st.columns(3)

submitted = left_column3.button("Translate")

clear = central_column3.button("clear", on_click=clear_text, key="model_output")

text_area = right_column2.empty()
text = text_area.text_area("Translation", height=200, max_chars=5000)


if submitted:
     text = text_area.text_area("Translation", translation, height=200, max_chars=5000, on_change=call_2, key='cic')


if clear:
    user_input = ""


done = right_column3.button("Done")
if done:
        text_input = sent_tokenize(user_input)
        text_output = sent_tokenize(st.session_state['sen'])
        path = "corpus/"+source_len+"_"+target_len+"_"+domain
        text = open(path, 'a')
        for i, j in zip(text_input, text_output):
            text.write(i+"\t "+j+"\n")


