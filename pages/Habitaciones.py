import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

st.set_page_config(page_icon="🛏️")

st.title("🛏️ GESTIÓN DE HABITACIONES")

def cargar_habitaciones():
    try:
        response = requests.get(f"{BASE_URL}/rooms/")
        if response.status_code == 200:
            rooms = response.json()
            if rooms:
                sorted_rooms = sorted(rooms, key=lambda x: x['room_id'])
                return [{
                    "ID": r['room_id'],
                    "Número": r['room_number'],
                    "Tipo": r['type'],
                    "Precio": r['price'],
                    "Estado": r['status']
                } for r in sorted_rooms]
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

st.header("Registrar Habitaciones")

if 'room_file_uploader_key' not in st.session_state:
    st.session_state.room_file_uploader_key = 0

uploaded_file = st.file_uploader("Selecciona el archivo Excel", type=['xlsx', 'xls'], key=f"excel_uploader_{st.session_state.room_file_uploader_key}")

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
                
                required_columns = ['room_number', 'type', 'price', 'status']
                if not all(col in df.columns for col in required_columns):
                    st.error("El archivo no contiene las columnas requeridas")
                    st.stop()

                # Convertir room_number a string
                df['room_number'] = df['room_number'].astype(str)
                
                rooms_data = df[required_columns].to_dict('records')
                
                try:
                    response = requests.post(f"{BASE_URL}/rooms/", json=rooms_data)
                    if response.status_code == 200:
                        st.success(f'Se registraron {len(rooms_data)} habitaciones exitosamente')
                        st.session_state.rooms_data = cargar_habitaciones()
                        st.session_state.room_file_uploader_key += 1
                        st.rerun()
                    else:
                        st.error(f'Error al registrar habitaciones: {response.text}')
                except Exception as e:
                    st.error(f"Error al registrar habitaciones: {str(e)}")
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

st.header("Lista de Habitaciones")

if 'rooms_data' not in st.session_state:
    with st.spinner('Cargando lista de habitaciones...'):
        st.session_state.rooms_data = cargar_habitaciones()

if st.session_state.rooms_data:
    st.dataframe(
        st.session_state.rooms_data,
        hide_index=True,
    )
else:
    st.info("No hay habitaciones registradas en el sistema") 