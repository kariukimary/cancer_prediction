import streamlit as st
import pickle
# import staging
from streamlit_extras.switch_page_button import switch_page

model = pickle.load(open('/home/mary/projects/fourth_year project/diagnose.pkl', 'rb'))

def cancer():
    st.title("Breast Cancer Prediction")

    col1, col2 = st.columns(2)  
    

    with col1:
        
        radius = st.text_input("Radius Mean")
        texture = st.text_input("Texture Mean")
        smoothness = st.text_input("Smoothness Mean")
        compactness = st.text_input("Compactness Mean")
        symmetry = st.text_input("Symmetry Mean")

    with col2:
       
        fractal = st.text_input("Fractal Dimension Mean")
        texturese = st.text_input("Texture SE")
        smoothnessse = st.text_input("Smoothness SE")
        symmetryse = st.text_input("Symmetry SE")
        symmetrywo = st.text_input("Symmetry Worst")

    if st.button('Predict'):
        # Making prediction
        makeprediction = model.predict([[radius, texture, smoothness, compactness, symmetry, fractal, texturese, smoothnessse, symmetryse, symmetrywo]])
        

        if makeprediction[0] == 1:
            st.success("You have breast cancer")
            button1 = st.button("switch")
            if button1:
                switch_page('patient')

        else:
            
            st.success("You don't have breast cancer")
            st.balloons()
                # if st.button("switch2patient"):
                #     switch_page("patient")
    # if st.button("stage"):
    #   prediction = model.predict([[radius, texture, smoothness, compactness, symmetry, fractal, texturese, smoothnessse, symmetryse, symmetrywo]])
    #   if prediction[0] == 1:
    #     switch_page('staging')
    #   else:
    #     switch_page("patient")


  

if __name__ == "__main__":
    cancer()
