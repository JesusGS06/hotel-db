import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

st.set_page_config(page_icon="📅")

st.title("📅 GESTIÓN DE RESERVACIONES")

def cargar_reservaciones():
    try:
        response = requests.get(f"{BASE_URL}/reservations/")
        if response.status_code == 200:
            reservations = response.json()
            if reservations:
                sorted_reservations = sorted(reservations, key=lambda x: x['reservation_id'])
                return [{
                    "ID": r['reservation_id'],
                    "Cliente ID": r['client_id'],
                    "Habitación ID": r['room_id'],
                    "Fecha Inicio": r['start_date'],
                    "Fecha Fin": r['end_date']
                } for r in sorted_reservations]
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

st.header("Registrar Reservaciones")

if 'reservation_file_uploader_key' not in st.session_state:
    st.session_state.reservation_file_uploader_key = 0

uploaded_file = st.file_uploader("Selecciona el archivo Excel", type=['xlsx', 'xls'], 
                               key=f"excel_uploader_{st.session_state.reservation_file_uploader_key}")

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
                
                required_columns = ['client_id', 'room_id', 'start_date', 'end_date']
                if not all(col in df.columns for col in required_columns):
                    st.error("El archivo no contiene las columnas requeridas")
                    st.stop()

                df['start_date'] = pd.to_datetime(df['start_date']).dt.strftime('%Y-%m-%d')
                df['end_date'] = pd.to_datetime(df['end_date']).dt.strftime('%Y-%m-%d')
                reservations_data = df[required_columns].to_dict('records')
                
                try:
                    response = requests.post(f"{BASE_URL}/reservations/", json=reservations_data)
                    if response.status_code == 200:
                        st.success(f'Se registraron {len(reservations_data)} reservaciones exitosamente')
                        st.session_state.reservations_data = cargar_reservaciones()
                        st.session_state.reservation_file_uploader_key += 1
                        st.rerun()
                    else:
                        st.error(f'Error al registrar reservaciones: {response.text}')
                except Exception as e:
                    st.error(f"Error al registrar reservaciones: {str(e)}")
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

st.header("Lista de Reservaciones")

if 'reservations_data' not in st.session_state:
    with st.spinner('Cargando lista de reservaciones...'):
        st.session_state.reservations_data = cargar_reservaciones()

if st.session_state.reservations_data:
    st.dataframe(
        st.session_state.reservations_data,
        hide_index=True,
    )
else:
    st.info("No hay reservaciones registradas en el sistema") 