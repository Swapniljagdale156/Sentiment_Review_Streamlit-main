from ctypes import alignment
import streamlit as st
import pickle
import re
from afinn import Afinn
af= Afinn(language='en', emoticons=False, word_boundary=True)

def text_cleaner (text):
    cleaned= re.sub('[^a-zA-Z]', " ", text) 
    cleaned= cleaned.lower()
    cleaned = cleaned.split()
    cleaned= ' '.join(cleaned)
    return cleaned


cv= pickle.load(open("vectorize.pkl", "rb"))
model = pickle.load(open("voting_classifier.pkl", "rb"))

st.header("Welocme to Review Analyzer of washing machine, We’re so happy you’re here!")


col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image("Was.png", width=200)


input_review = st.text_area("The concept is simple: You just enter the review and we will let you know the sentiment behind it, which will help you to Grow, Survive & Thrive")
if st.button("Predict"):
    try:
        if len([input_review])>2:
            cleaned_review= text_cleaner(input_review)
            cv_r= cv.transform([cleaned_review])
            result= model.predict(cv_r)
            if result==1:
                st.image("happy.png", width=70) 
                st.header("Hey, its Positive Review !!!")
                st.header("Great, Keep it up")
            else:
                st.image("sad.png",width=50) 
                st.header("Sadly, its Negative Review!")
                st.header("There is scope for improvement")
        else:
            lst = (input_review).split()
            if len(lst)==1:
                score=af.score(lst[0].lower())
            else:    
                for word in (lst):
                    if lst[0].lower()=="not":
                        score = af.score(lst[1])*(-1)
                    else:
                        score = af.score(lst[0]) + (af.score(lst[1]))
            if score>=0:
                st.image("happy.png", width=70) 
                st.header("Hey, its Positive Review !!!")
                st.header("Great, Keep it up")
            else:
                st.image("sad.png",width=50) 
                st.header("Sadly, its Negative Review!")
                st.header("There is scope for improvement")
    except:
        pass            

