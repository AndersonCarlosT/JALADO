import streamlit as st
import pandas as pd

st.set_page_config(page_title="📄 Buscador en archivo Excel", layout="centered")
st.title("🔍 Buscar datos por Código en Excel")

excel_file = st.file_uploader("Sube un archivo Excel", type=["xlsx"])

codigo_input = st.text_input("🔢 Ingresa el Código a buscar (número exacto):")

if excel_file and codigo_input:
    try:
        df = pd.read_excel(excel_file, usecols=[0, 1, 2])
        df.columns = ["Código", "Fecha", "Precio"]

        resultado = df[df["Código"].astype(str) == codigo_input.strip()]
        
        if not resultado.empty:
            st.success("✅ Código encontrado:")
            st.dataframe(resultado)
        else:
            st.warning("⚠ No se encontró ese código en el archivo.")

    except Exception as e:
        st.error(f"❌ Error leyendo el archivo: {str(e)}")
