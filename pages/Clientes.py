import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000"

st.set_page_config(page_icon="👥")

st.title("👥 GESTIÓN DE CLIENTES")

def cargar_clientes():
    try:
        response = requests.get(f"{BASE_URL}/clients/")
        if response.status_code == 200:
            clients = response.json()
            if clients:
                sorted_clients = sorted(clients, key=lambda x: x['client_id'])
                return [{
                    "ID": c['client_id'],
                    "Nombre": c['first_name'],
                    "Apellido": c['last_name'],
                    "Email": c['email'],
                    "Teléfono": c['phone']
                } for c in sorted_clients]
            return None
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
        return None

st.header("Crear Clientes")

if 'file_uploader_key' not in st.session_state:
    st.session_state.file_uploader_key = 0

uploaded_file = st.file_uploader("Selecciona el archivo Excel", type=['xlsx', 'xls'], key=f"excel_uploader_{st.session_state.file_uploader_key}")

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
                
                required_columns = ['first_name', 'last_name', 'email', 'phone']
                if not all(col in df.columns for col in required_columns):
                    st.error("El archivo no contiene las columnas requeridas")
                    st.stop()

                df['phone'] = df['phone'].astype(str)
                clientes_data = df[required_columns].to_dict('records')
                
                try:
                    response = requests.post(f"{BASE_URL}/clients/", json=clientes_data)
                    if response.status_code == 200:
                        st.success(f'Se crearon {len(clientes_data)} clientes exitosamente')
                        st.session_state.data = cargar_clientes()
                        st.session_state.file_uploader_key += 1
                        st.rerun()
                    else:
                        st.error(f'Error al crear clientes: {response.text}')
                except Exception as e:
                    st.error(f"Error al crear clientes: {str(e)}")
            
        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")

st.header("Lista de Clientes")

if 'data' not in st.session_state:
    with st.spinner('Cargando lista de clientes...'):
        st.session_state.data = cargar_clientes()

if st.session_state.data:
    st.dataframe(
        st.session_state.data,
        hide_index=True, 
    )
else:
    st.info("No hay clientes registrados en el sistema")