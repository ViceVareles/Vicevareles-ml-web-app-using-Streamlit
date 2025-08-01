import streamlit as st
import pickle
import numpy as np

# Botón para reiniciar formulario (esquina superior derecha)
with st.sidebar:
    st.title("⚙️ Opciones")
    if st.button("🔄 Reiniciar formulario"):
        st.experimental_rerun()

# Cargar modelo
def load_model():
    with open("decision_tree_classifier_default_42.sav", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

st.title("🧬 Predicción de Diabetes")
st.markdown("Introduce los datos del paciente para predecir si tiene diabetes.")

# Inputs del usuario
pregnancies = st.number_input("Número de embarazos", min_value=0, max_value=20, value=1)
glucose = st.number_input("Nivel de glucosa", min_value=0, max_value=300, value=100)
blood_pressure = st.number_input("Presión arterial", min_value=0, max_value=180, value=70)
skin_thickness = st.number_input("Espesor del pliegue cutáneo", min_value=0, max_value=100, value=20)
insulin = st.number_input("Nivel de insulina", min_value=0, max_value=1000, value=80)
bmi = st.number_input("Índice de masa corporal (BMI)", min_value=0.0, max_value=100.0, value=25.0, format="%.1f")
dpf = st.number_input("Función de pedigrí diabético", min_value=0.0, max_value=3.0, value=0.5, format="%.3f")
age = st.number_input("Edad", min_value=0, max_value=120, value=35)

# Validación de rangos
valido = True

if glucose < 50:
    st.warning("⚠️ El nivel de glucosa es demasiado bajo para ser real.")
    valido = False
if blood_pressure < 40:
    st.warning("⚠️ La presión arterial es muy baja.")
    valido = False
if insulin < 10:
    st.warning("⚠️ Un valor de insulina tan bajo suele indicar datos faltantes.")
    valido = False
if bmi < 10:
    st.warning("⚠️ El BMI está fuera del rango saludable o es inválido.")
    valido = False
if age < 10:
    st.warning("⚠️ Edad sospechosamente baja.")
    valido = False

# Botón de predicción
if st.button("Predecir"):
    if valido:
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                                insulin, bmi, dpf, age]])
        prediction = model.predict(input_data)
        resultado = "🔴 Positivo: Diabetes" if prediction[0] == 1 else "🟢 Negativo: No diabetes"
        st.success(f"Resultado: {resultado}")
    else:
        st.error("❌ Corrige los valores inválidos antes de continuar con la predicción.")