import streamlit as st
import pandas as pd
from utils import load_data

def main():
    st.title("Mi Aplicación Streamlit")
    
    data = load_data("data.csv")
    
    st.write("Datos cargados:")
    st.dataframe(data)

    if st.button("Mostrar estadísticas"):
        st.write(data.describe())

if __name__ == "__main__":
    main()