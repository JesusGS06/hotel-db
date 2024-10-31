import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

def test_api_connection():  
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            st.info('API conectada correctamente')
            return True
        else:
            st.error("Error al conectar con la API")
            return False
    except requests.exceptions.ConnectionError:
        st.error("No se puede conectar con la API")
        return False

def main():

    st.title("Sistema de Gestión Hotelera")
    
    if not test_api_connection():
        st.warning("Por favor, asegúrate de que el servidor FastAPI esté corriendo en http://localhost:8000")
        return

    st.write("Bienvenido al Sistema de Gestión Hotelera")
    
    st.header("Módulos Disponibles")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gestión de Clientes y Habitaciones")
        st.write("- Registro y consulta de clientes")
        st.write("- Gestión de habitaciones")
        st.write("- Estado de habitaciones")
    
    with col2:
        st.subheader("Reservaciones y Servicios")
        st.write("- Gestión de reservaciones")
        st.write("- Servicios adicionales")
        st.write("- Registro de pagos")
    
    st.header("Características")
    st.write("✅ Carga masiva de datos mediante Excel")
    st.write("✅ Visualización de registros en tiempo real")
    st.write("✅ Gestión de mantenimiento de habitaciones")
    st.write("✅ Control de pagos y servicios")

    st.info("""
    Utiliza el menú lateral para navegar entre las diferentes secciones del sistema.
    Cada módulo permite la carga de datos mediante archivos Excel y visualización de registros.
    """)

if __name__ == "__main__":
    main() 