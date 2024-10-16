import streamlit as st
import pandas as pd
import os
import ast
import time


file_path = os.path.abspath("dataset\movies.csv")
movies = pd.read_csv(file_path).head(10)
movies['genre'] = movies['genre'].apply(ast.literal_eval)

st.title("Top 10 IMDb movies")

title = st.empty()
c1, c2 = st.columns(2)
genre = st.empty()
year = st.empty()
description = st.empty()
rating = st.empty()
progressbar = st.progress(0)

i = 0
while True:
  cur = movies.iloc[i]
  title.write("""## {}""".format(cur['title']))

  with c1:
    genre.write("""**Genre:** _{}_""".format(', '.join(cur['genre'])))
  with c2:
    year.write("""**Year:** {}""".format(cur['year']))

  description.write("""
  #### Description
  {}
  """.format(cur['description']))

  rating.write("""**Rating:** {}/10""".format(cur['rating']))

  progressbar.progress(0)
  duration = 5
  for j in range(100):
    progressbar.progress((j + 1) / 100)
    time.sleep(duration / 100)
  progressbar.empty()
  time.sleep(0.05)

  i = (i + 1) % 10
