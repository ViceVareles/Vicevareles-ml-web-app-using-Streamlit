import streamlit as st
import pickle
import numpy as np

# Cargar el modelo
def load_model():
    with open("decision_tree_classifier_default_42.sav", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

st.title("🧬 Predicción de Diabetes")
st.markdown("Introduce los datos del paciente para predecir si tiene diabetes.")

# Inicializar el historial si no existe
if "history" not in st.session_state:
    st.session_state["history"] = []

# Reiniciar los campos del formulario
def reset_form():
    for field in ["pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin", "bmi", "dpf", "age"]:
        st.session_state[field] = 0  # valor por defecto

# Crear el formulario
with st.form("formulario_diabetes"):
    st.subheader("📝 Datos del paciente")

    pregnancies = st.number_input("Número de embarazos", min_value=0, max_value=20, key="pregnancies", value=1)
    glucose = st.number_input("Nivel de glucosa", min_value=0, max_value=300, key="glucose", value=100)
    blood_pressure = st.number_input("Presión arterial", min_value=0, max_value=180, key="blood_pressure", value=70)
    skin_thickness = st.number_input("Espesor del pliegue cutáneo", min_value=0, max_value=100, key="skin_thickness", value=20)
    insulin = st.number_input("Nivel de insulina", min_value=0, max_value=1000, key="insulin", value=80)
    bmi = st.number_input("Índice de masa corporal (BMI)", min_value=0.0, max_value=100.0, format="%.1f", key="bmi", value=25.0)
    dpf = st.number_input("Función de pedigrí diabético", min_value=0.0, max_value=3.0, format="%.3f", key="dpf", value=0.5)
    age = st.number_input("Edad", min_value=0, max_value=120, key="age", value=35)

    col1, col2 = st.columns(2)
    submit = col1.form_submit_button("✅ Predecir")
    reset = col2.form_submit_button("🔄 Reiniciar")

# Procesar acciones después del formulario
if submit:
    valido = True

    if glucose < 50:
        st.warning("⚠️ El nivel de glucosa es demasiado bajo.")
        valido = False
    if blood_pressure < 40:
        st.warning("⚠️ Presión arterial muy baja.")
        valido = False
    if insulin < 10:
        st.warning("⚠️ Insulina muy baja.")
        valido = False
    if bmi < 10:
        st.warning("⚠️ BMI fuera de rango.")
        valido = False
    if age < 10:
        st.warning("⚠️ Edad sospechosamente baja.")
        valido = False

    if valido:
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                                insulin, bmi, dpf, age]])
        prediction = model.predict(input_data)
        resultado = "🔴 Positivo: Diabetes" if prediction[0] == 1 else "🟢 Negativo: No diabetes"
        st.success(f"Resultado: {resultado}")

        # Guardar en el historial
        st.session_state["history"].append({
            "Embarazos": pregnancies,
            "Glucosa": glucose,
            "Presión": blood_pressure,
            "Piel": skin_thickness,
            "Insulina": insulin,
            "BMI": bmi,
            "Pedigrí": dpf,
            "Edad": age,
            "Resultado": resultado
        })
    else:
        st.error("❌ Corrige los datos antes de continuar.")

elif reset:
    reset_form()
    st.rerun()

# Mostrar historial si hay
if st.session_state["history"]:
    st.markdown("### 📊 Historial de predicciones")
    st.dataframe(st.session_state["history"])