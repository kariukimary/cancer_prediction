import streamlit as st
import pickle
import mysql.connector
import numpy as np


model = pickle.load(open('cancer_stage.pkl', 'rb'))


def connect_to_database():
    conn = mysql.connector.connect(
        host=" sql6.freesqldatabase.com",
        user="sql6695216",
        password="xE87WYUisq",
        database="sql6695216"
    )
    return conn


def save_user_inputs(T_stage, N_stage, grade, a_stage, tumor_size, estrogen_status, progesterone, regional_node_examined, regional_node_positive, predicted_stage):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO user_records (T, N, G, A, tumor_size, estrogen_status, progesterone_status, regional_node_examined, regional_node_positive, predicted_stage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (T_stage, N_stage, grade, a_stage, tumor_size, estrogen_status, progesterone, regional_node_examined, regional_node_positive, predicted_stage))
        conn.commit()
        cursor.close()
        conn.close()


def stages():
    st.title("Breast Cancer Stage Prediction")

  
    col1, col2 = st.columns(2)  

    with col1:
        T_options = ['T1', 'T2', 'T3', 'T4']
        T = st.selectbox("T: (tumor stage)", T_options)

        N_options = ['N1', 'N2', 'N3']
        N = st.selectbox("N: (nodal stage)", N_options)

        G_options = ['Well differentiated; Grade I', 'Moderately differentiated; Grade II', 'Poorly differentiated; Grade III', 'Undifferentiated; anaplastic; Grade IV']
        G = st.selectbox("G: (grade of the tumor under microscope)", G_options)

        A_options = ['Regional', 'Distant']
        A = st.selectbox("A: (extent of disease)", A_options)
        tumor_size = st.number_input("Tumor Size: (size of the tumor)")
    
    with col2:
        estrogen_status_options = ['positive', 'negative']
        estrogen_status = st.selectbox("Estrogen Status:(receptors for estrogen)", estrogen_status_options)

        progesterone_options = ['positive', 'negative']
        progesterone = st.selectbox("Progesterone Status: (receptors for progesterone)", progesterone_options)

        regional_node_examined = st.number_input("Regional Node Examined: (lymph nodes )")
        regional_node_positive = st.number_input("Regional Node Positive: (positive lymph nodes )")

   
    T_mapping = {'T1': 0, 'T2': 1, 'T3': 2, 'T4': 3}
    N_mapping = {'N1': 0, 'N2': 1, 'N3': 2}
    G_mapping = {'Well differentiated; Grade I': 1, 'Moderately differentiated; Grade II': 2,
                     'Poorly differentiated; Grade III': 3, 'Undifferentiated; anaplastic; Grade IV': 4}
    A_mapping = {'Regional': 1, 'Distant': 0}
    estrogen_status_mapping = {'positive': 1, 'negative': 0}
    progesterone_mapping = {'positive': 1, 'negative': 0}

    T_stage = T_mapping.get(T, 0)
    N_stage = N_mapping.get(N, 0)
    grade = G_mapping.get(G, 0)
    a_stage = A_mapping.get(A, 0)  
    estrogen_status_encoded = estrogen_status_mapping.get(estrogen_status, 0)
    progesterone_encoded = progesterone_mapping.get(progesterone, 0)

    if st.button('Predict', key='predict_button'):
        input_data = [
            [T_stage, N_stage, grade, a_stage, tumor_size, estrogen_status_encoded, progesterone_encoded, regional_node_examined, regional_node_positive]
        ]
        
        predicted_stage = model.predict(input_data)[0]
        st.success(f'You are in Stage {predicted_stage}')

    
        predicted_stage = int(predicted_stage)

       
        save_user_inputs(T, N, G, A, tumor_size, estrogen_status, progesterone, regional_node_examined, regional_node_positive, predicted_stage)


if __name__ == '__main__':
    stages()
