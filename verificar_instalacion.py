import sys
import pkg_resources

def verificar_instalacion():
    print("🔍 Verificando instalación de paquetes...")
    
    paquetes = ["supabase", "python-dotenv", "httpx"]
    
    for paquete in paquetes:
        try:
            version = pkg_resources.get_distribution(paquete).version
            print(f"✅ {paquete}: {version}")
        except:
            print(f"❌ {paquete}: NO INSTALADO")
    
    print(f"✅ Python: {sys.version}")

if __name__ == "__main__":
    verificar_instalacion()

    