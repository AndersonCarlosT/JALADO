import streamlit as st
import pandas as pd

st.set_page_config(page_title="📄 Buscar Código en múltiples Excels", layout="centered")
st.title("🔍 Buscar datos por Código en múltiples archivos Excel")

excel_files = st.file_uploader("📂 Sube uno o más archivos Excel", type=["xlsx"], accept_multiple_files=True)
codigo_input = st.text_input("🔢 Ingresa el Código a buscar (número exacto):")

if excel_files and codigo_input:
    resultados = []

    for file in excel_files:
        try:
            df = pd.read_excel(file, usecols=[0, 1, 2])
            df.columns = ["Código", "Fecha", "Precio"]

            # Convertir fechas correctamente
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce')
            df = df.dropna(subset=["Fecha"])
            df["Fecha"] = df["Fecha"].dt.strftime("%d/%m/%Y")

            # Buscar coincidencias
            coincidencias = df[df["Código"].astype(str) == codigo_input.strip()]
            if not coincidencias.empty:
                resultados.append(coincidencias)

        except Exception as e:
            st.error(f"❌ Error con el archivo {file.name}: {str(e)}")

    if resultados:
        final_df = pd.concat(resultados, ignore_index=True)
        st.success("✅ Código encontrado:")
        st.dataframe(final_df[["Código", "Fecha", "Precio"]])
    else:
        st.warning("⚠ No se encontró el código en ningún archivo.")
