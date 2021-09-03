# pylint: disable = E1121
# pylint: disable = W0703
# pylint: disable = C0114
# pylint: disable = C0206


import streamlit as st
import speech_recognition as sr
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def markdown_runner(md_code):
    """ A function to run HTML in MD code """
    st.markdown(md_code, unsafe_allow_html=True)


def intro_func():
    """ provides title and intro """
    title_text = '''<p style="font-size:45px;"> Welcome to
            <span style='color:blue'> D. Analyzer </span></p>'''
    markdown_runner(title_text)
    st.subheader("It can help in analyzing text form files and audio as well")


def decorator(func):
    """ A decorator function to decorate the output """
    def inner(section_name, *args, **kwargs):
        markdown_runner(
            f"""<p style="font_size:25px"> {section_name} </p>""")
        func(*args, **kwargs)
        markdown_runner("""<hr/>""")
    return inner


def speech_to_text(file):
    """ Function to convert speech/audio to text/string """
    rec = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = rec.record(source)
        try:
            text = rec.recognize_google(audio)
        except Exception as error:
            st.write(error)
    return text


@decorator
def display_input(message):
    """ Function to display the given input in text form """
    st.write(message)


@decorator
def sentiment_analyzer(message):
    """
        A function to analyze sentiments
        It can be +ve, -ve, N, C
    """
    sid = SentimentIntensityAnalyzer()
    scores_raw = sid.polarity_scores(message)
    new_keys = ["negative", "neutral", "positive", "compound"]
    scores = dict(zip(new_keys, list(scores_raw.values())))
    score_lst = [[key, value] for key, value in scores.items() if value > 0]

    for type_of_sentiment, value_of_it in score_lst:
        st.write(
            f"""Sentiment type {type_of_sentiment} and
                percentage of it is {round((value_of_it * 100), 2)}""")


@decorator
def word_cloud(message, selected_word_count):
    """ Function to make word cloud based on the given inputs """
    stopword = set(STOPWORDS)

    wordcloud = WordCloud(background_color="white",
                          max_words=selected_word_count, stopwords=stopword).generate(message)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.show()
    st.pyplot()


@decorator
def text_summarizer(text):
    """
        This function will try to summarize
        the text for you based on cosine prob.
    """
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)

    freq_table = dict()
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1

    sentences = sent_tokenize(text)
    sentence_value = dict()

    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq

    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]

    average = int(sum_values / len(sentence_value))

    summary = ''
    for sentence in sentences:
        if (sentence in sentence_value) and (sentence_value[sentence] > (1.2 * average)):
            summary += " " + sentence
    if summary != "":
        st.write(summary)
    else:
        st.write("File too short")


@decorator
def text_descreption(message):
    """ To provide the basic descp. of text """

    num_lines = len(message.split("\n"))
    num_words = len(message.split())

    num_char = 0

    for _ in message:
        num_char += 1

    st.write("Number of words in text file: ", num_words)
    st.write("Number of characters in text file: ", num_char)
    st.write("Number of lines in text file: ", num_lines)


@decorator
def word_finder(find_word, message):
    """ A function to find word in given text """
    find_word = find_word.strip()

    if find_word is not None and find_word in message:
        st.success(f"The given word {find_word} is Found!!")
        find_word_highlight = f"""<span style="color:red">{find_word}</span>"""
        occurences = message.replace(find_word, find_word_highlight)
        markdown_runner(occurences)

    else:
        st.error(f"The given word {find_word} is not Found!!")


@decorator
def play_audio(audio_bytes):
    """ A function to show to audio provided as input"""
    st.audio(audio_bytes, format=r'audio/ogg')


def analyser(message, selected_word_count, find_word):
    """
        It is the function that will invoke all other functions
        to perform analysis on data
    """
    sentiment_analyzer("Sentiment Analyzer", message)
    word_cloud("Word Cloud", message, selected_word_count)
    display_input("Given Input Data", message)
    text_descreption("Text Description", message)
    text_summarizer("Text Summary", message)

    if find_word is not None:
        word_finder("Word Finder", find_word, message)


def text_analysis(selected_word_count, find_word):
    """ Mode based function sends text to analyzer"""
    markdown_runner(
        """<p style="font_size:22px"> Text Analyzer Mode Selected </p>""")
    markdown_runner("""<hr/>""")
    markdown_runner("""<p style="font_size:25px"> Upload Data </p>""")

    file_bytes = st.file_uploader("uplaod a text file", type="txt", key="1")

    if file_bytes is not None:
        st.success(f"Successfully Uploaded {file_bytes.name}")
        markdown_runner("""<hr/>""")

        message = file_bytes.read().decode()
        analyser(message, selected_word_count, find_word)


def speech_analysis(selected_word_count, find_word):
    """
        Mode based function
        firts invokes speech to text
        and then sends text to analyzer
    """
    markdown_runner(
        """<p style="font_size:22px"> Speech Analyzer Mode Selected </p>""")
    markdown_runner("""<hr/>""")
    markdown_runner("""<p style="font_size:25px"> Upload Data </p>""")

    file_bytes = st.file_uploader("uplaod a text file", type="wav", key="1")

    if file_bytes is not None:
        st.success(f"Successfully Uploaded {file_bytes.name}")
        markdown_runner("""<hr/>""")
        play_audio("Given Audio Input", file_bytes)
        message = speech_to_text(file_bytes)
        analyser(message, selected_word_count, find_word)


modes = ["Audio input", "Text file input"]


def input_mode(mode_type, selected_word_count, find_words):
    """ mode selector for Streamlit app """
    if mode_type == modes[1]:
        text_analysis(selected_word_count, find_words)

    else:
        speech_analysis(selected_word_count, find_words)


def setter_func():
    """ The MAIN function.... """
    st.sidebar.header("Select Input Mode")
    selected_mode = st.sidebar.selectbox('Modes', modes)

    st.sidebar.header("Select number of words you want to use")
    selected_word_count = st.sidebar.selectbox(
        "No of words", range(10, 1000, 10))

    typ = ["Yes", "No"]
    st.sidebar.header("Are you looking for a specific word or phrase")
    find_words = st.sidebar.radio("Select", typ)

    if find_words in typ[0]:
        find_word = st.sidebar.text_input("Enter here", value=None)

    else:
        find_word = None

    st.sidebar.header("Click here to exit")
    st.sidebar.button("Exit")

    input_mode(selected_mode, selected_word_count, find_word)


if __name__ == '__main__':
    intro_func()
    setter_func()
