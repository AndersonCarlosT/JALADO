import streamlit as st
import pandas as pd

st.set_page_config(page_title="📄 Buscar múltiples códigos en Excels", layout="centered")
st.title("🔍 Buscar múltiples códigos en archivos Excel")

excel_files = st.file_uploader("📂 Sube uno o más archivos Excel", type=["xlsx"], accept_multiple_files=True)

codigos_input = st.text_area("🔢 Ingresa uno o más códigos separados por coma o salto de línea:")

if excel_files and codigos_input:
    # Limpieza y conversión de los códigos ingresados
    codigos = [c.strip() for c in codigos_input.replace(",", "\n").splitlines() if c.strip()]
    
    if not codigos:
        st.warning("⚠ Por favor, ingresa al menos un código válido.")
    else:
        resultados = []

        for file in excel_files:
            try:
                df = pd.read_excel(file, usecols=[0, 1, 2])
                df.columns = ["Código", "Fecha", "Precio"]

                # Formatear fechas
                df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce')
                df = df.dropna(subset=["Fecha"])
                df["Fecha"] = df["Fecha"].dt.strftime("%d/%m/%Y")

                # Filtrar solo los códigos que el usuario ingresó
                coincidencias = df[df["Código"].astype(str).isin(codigos)]
                if not coincidencias.empty:
                    resultados.append(coincidencias)

            except Exception as e:
                st.error(f"❌ Error con el archivo {file.name}: {str(e)}")

        if resultados:
            final_df = pd.concat(resultados, ignore_index=True)
            st.success("✅ Resultados encontrados:")
            st.dataframe(final_df[["Código", "Fecha", "Precio"]])
        else:
            st.warning("⚠ No se encontraron coincidencias en ningún archivo.")
