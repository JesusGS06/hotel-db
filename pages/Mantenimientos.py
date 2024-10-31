import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

st.set_page_config(page_icon="🔧")

st.title("🔧 GESTIÓN DE MANTENIMIENTO")

def cargar_mantenimientos():
    try:
        response = requests.get(f"{BASE_URL}/maintenance/")
        if response.status_code == 200:
            records = response.json()
            if records:
                sorted_records = sorted(records, key=lambda x: x['maintenance_id'])
                return [{
                    "ID": m['maintenance_id'],
                    "Habitación ID": m['room_id'],
                    "Fecha": m['maintenance_date'],
                    "Descripción": m['description']
                } for m in sorted_records]
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

st.header("Registrar Mantenimientos")

if 'maintenance_file_uploader_key' not in st.session_state:
    st.session_state.maintenance_file_uploader_key = 0

uploaded_file = st.file_uploader("Selecciona el archivo Excel", type=['xlsx', 'xls'], 
                               key=f"excel_uploader_{st.session_state.maintenance_file_uploader_key}")

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
                
                required_columns = ['room_id', 'maintenance_date', 'description']
                if not all(col in df.columns for col in required_columns):
                    st.error("El archivo no contiene las columnas requeridas")
                    st.stop()

                df['maintenance_date'] = pd.to_datetime(df['maintenance_date']).dt.strftime('%Y-%m-%d')
                
                maintenance_data = df[required_columns].to_dict('records')
                
                try:
                    response = requests.post(f"{BASE_URL}/maintenance/", json=maintenance_data)
                    if response.status_code == 200:
                        st.success(f'Se registraron {len(maintenance_data)} mantenimientos exitosamente')
                        st.session_state.maintenance_data = cargar_mantenimientos()
                        st.session_state.maintenance_file_uploader_key += 1
                        st.rerun()
                    else:
                        st.error(f'Error al registrar mantenimientos: {response.text}')
                except Exception as e:
                    st.error(f"Error al registrar mantenimientos: {str(e)}")
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

st.header("Lista de Mantenimientos")

if 'maintenance_data' not in st.session_state:
    with st.spinner('Cargando lista de mantenimientos...'):
        st.session_state.maintenance_data = cargar_mantenimientos()

if st.session_state.maintenance_data:
    st.dataframe(
        st.session_state.maintenance_data,
        hide_index=True,
    )
else:
    st.info("No hay registros de mantenimiento en el sistema") 