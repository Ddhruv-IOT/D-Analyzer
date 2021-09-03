#import streamlit as st
#st.text("hccsi")

#title = '<p style="font-size:45px;"> HIIx </p>'
#st.markdown(title, unsafe_allow_html=True)

#st.header("1")
#st.subheader("2")
#st.title("3")
#st.markdown("4")
#st.success("5")
#st.warning("6")
#st.error("7")

#import pandas as pd 
#df = pd.read_csv("areas.csv")

#st.write(df)

#import plotly.express as px

#fb = st.file_uploader("uplaod a file", type="*")

import streamlit as st 
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import requests 
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import regex as re

st.title("WC APP")

st.sidebar.header("Select Link")
links = ["https://seaportai.com/industry4-0/", "https://seaportai.com/blog-rpameetsai/"]

url = st.sidebar.selectbox('Link', links)

st.sidebar.header("Select number of words you want to use")
words = st.sidebar.selectbox("No of words", range(10, 1000, 10))

if url is not None: 
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	table = soup.find('div', attrs = {'id':'main-content'})
	text = table.text
	cleaned_text = re.sub('\t',"",text)
	cleaned_texts = re.split('\n', cleaned_text)
	cleaned_textss ="".join(cleaned_texts)
	st.write(cleaned_textss)
	stopwords = set(STOPWORDS)
	wordcloud = WordCloud(background_color="white", max_words=words, stopwords=stopwords).generate(cleaned_textss)

	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	plt.show()
	st.pyplot(plt.show())