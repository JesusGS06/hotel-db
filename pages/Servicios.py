import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_icon="🛎️")

BASE_URL = "http://localhost:8000"

st.title("🛎️ GESTIÓN DE SERVICIOS")

def cargar_servicios():
    try:
        response = requests.get(f"{BASE_URL}/services/")
        if response.status_code == 200:
            services = response.json()
            if services:
                sorted_services = sorted(services, key=lambda x: x['service_id'])
                return [{
                    "ID": s['service_id'],
                    "Nombre": s['name'],
                    "Descripción": s['description'],
                    "Costo": s['cost']
                } for s in sorted_services]
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

st.header("Registrar Servicios")

if 'service_file_uploader_key' not in st.session_state:
    st.session_state.service_key = 0

uploaded_file = st.file_uploader("Selecciona el archivo Excel", type=['xlsx', 'xls'], key=f"excel_uploader_{st.session_state.service_key}")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    procesar_button = st.button("Procesar Excel", use_container_width=True)

if procesar_button:
    if not uploaded_file:
        st.warning("Por favor, selecciona un archivo Excel antes de procesar")
    else:
        try:
            with st.spinner("Procesando archivo Excel..."):
                df = pd.read_excel(uploaded_file)
                
                required_columns = ['name', 'description', 'cost']
                if not all(col in df.columns for col in required_columns):
                    st.error("El archivo no contiene las columnas requeridas")
                    st.stop()

                services_data = df[required_columns].to_dict('records')
                
                try:
                    response = requests.post(f"{BASE_URL}/services/", json=services_data)
                    if response.status_code == 200:
                        st.success(f'Se registraron {len(services_data)} servicios exitosamente')
                        st.session_state.services_data = cargar_servicios()
                        st.session_state.service_key += 1
                        st.rerun()
                    else:
                        st.error(f'Error al registrar servicios: {response.text}')
                except Exception as e:
                    st.error(f"Error al registrar servicios: {str(e)}")
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

st.header("Lista de Servicios")

if 'services_data' not in st.session_state:
    with st.spinner('Cargando lista de servicios...'):
        st.session_state.services_data = cargar_servicios()

if st.session_state.services_data:
    st.dataframe(
        st.session_state.services_data,
        hide_index=True,
    )
else:
    st.info("No hay servicios registrados en el sistema") 