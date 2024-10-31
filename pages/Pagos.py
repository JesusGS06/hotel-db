import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

st.set_page_config(page_icon="💰")

st.title("💰 GESTIÓN DE PAGOS")

def cargar_pagos():
    try:
        response = requests.get(f"{BASE_URL}/payments/")
        if response.status_code == 200:
            payments = response.json()
            if payments:
                sorted_payments = sorted(payments, key=lambda x: x['payment_id'])
                return [{
                    "ID": p['payment_id'],
                    "Reservación ID": p['reservation_id'],
                    "Monto": p['amount'],
                    "Fecha": p['payment_date'],
                    "Método": p['payment_method']
                } for p in sorted_payments]
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

st.header("Registrar Pagos")

if 'payment_file_uploader_key' not in st.session_state:
    st.session_state.payment_file_uploader_key = 0

uploaded_file = st.file_uploader("Selecciona el archivo Excel", type=['xlsx', 'xls'], 
                               key=f"excel_uploader_{st.session_state.payment_file_uploader_key}")

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
                
                required_columns = ['reservation_id', 'amount', 'payment_date', 'payment_method']
                if not all(col in df.columns for col in required_columns):
                    st.error("El archivo no contiene las columnas requeridas")
                    st.stop()

                df['payment_date'] = pd.to_datetime(df['payment_date']).dt.strftime('%Y-%m-%d')
                
                payments_data = df[required_columns].to_dict('records')
                
                try:
                    response = requests.post(f"{BASE_URL}/payments/", json=payments_data)
                    if response.status_code == 200:
                        st.success(f'Se registraron {len(payments_data)} pagos exitosamente')
                        st.session_state.payments_data = cargar_pagos()
                        st.session_state.payment_file_uploader_key += 1
                        st.rerun()
                    else:
                        st.error(f'Error al registrar pagos: {response.text}')
                except Exception as e:
                    st.error(f"Error al registrar pagos: {str(e)}")
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

st.header("Lista de Pagos")

if 'payments_data' not in st.session_state:
    with st.spinner('Cargando lista de pagos...'):
        st.session_state.payments_data = cargar_pagos()

if st.session_state.payments_data:
    st.dataframe(
        st.session_state.payments_data,
        hide_index=True,
    )
else:
    st.info("No hay pagos registrados en el sistema") 