import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def test_simple():
    """Prueba de conexión simple"""
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        print(f"URL: {url}")
        print(f"KEY: {key[:20]}...")  # Mostrar solo parte de la key por seguridad
        
        # Crear cliente
        client = create_client(url, key)
        
        # Probar consulta simple
        response = client.table("dueno").select("*").limit(1).execute()
        print("CONEXIÓN EXITOSA!")
        print(f"Datos: {response.data}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_simple()