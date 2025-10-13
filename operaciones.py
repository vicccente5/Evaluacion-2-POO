from supabase_client import supabase
from datetime import datetime

# ========== OPERACIONES PARA DUEÑOS ==========
def crear_dueno(nombre, direccion, telefono, email):
    """Crear nuevo dueño"""
    try:
        datos = {
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono,
            "email": email
        }
        resultado = supabase.table("dueno").insert(datos).execute()
        if resultado.data:
            print(f"✅ Dueño '{nombre}' creado con ID: {resultado.data[0]['id_dueno']}")
            return resultado.data[0]['id_dueno']
        return None
    except Exception as e:
        print(f"Error creando dueño: {e}")
        return None

def obtener_duenos():
    """Obtener todos los dueños"""
    try:
        resultado = supabase.table("dueno").select("*").order("id_dueno").execute()
        return resultado.data
    except Exception as e:
        print(f"Error obteniendo dueños: {e}")
        return []

def buscar_dueno_por_nombre(nombre):
    """Buscar dueños por nombre"""
    try:
        resultado = supabase.table("dueno").select("*").ilike("nombre", f"%{nombre}%").execute()
        return resultado.data
    except Exception as e:
        print(f"Error buscando dueño: {e}")
        return []

def actualizar_dueno(id_dueno, nuevos_datos):
    """Actualizar dueño"""
    try:
        resultado = supabase.table("dueno").update(nuevos_datos).eq("id_dueno", id_dueno).execute()
        if resultado.data:
            print(f"✅ Dueño ID {id_dueno} actualizado")
        return resultado.data
    except Exception as e:
        print(f"Error actualizando dueño: {e}")
        return None

# ========== OPERACIONES PARA MASCOTAS ==========
def crear_mascota(nombre, especie, raza, fecha_nacimiento, id_dueno):
    """Crear nueva mascota"""
    try:
        datos = {
            "nombre": nombre,
            "especie": especie,
            "raza": raza,
            "fecha_nacimiento": fecha_nacimiento,
            "id_dueno": id_dueno
        }
        resultado = supabase.table("mascota").insert(datos).execute()
        if resultado.data:
            print(f"Mascota '{nombre}' creada con ID: {resultado.data[0]['id_mascota']}")
            return resultado.data[0]['id_mascota']
        return None
    except Exception as e:
        print(f"Error creando mascota: {e}")
        return None

def obtener_mascotas():
    """Obtener todas las mascotas con info del dueño"""
    try:
        resultado = supabase.table("mascota").select("*, dueno(nombre, telefono)").order("id_mascota").execute()
        return resultado.data
    except Exception as e:
        print(f"Error obteniendo mascotas: {e}")
        return []

def obtener_mascotas_por_dueno(id_dueno):
    """Obtener mascotas de un dueño específico"""
    try:
        resultado = supabase.table("mascota").select("*").eq("id_dueno", id_dueno).execute()
        return resultado.data
    except Exception as e:
        print(f"Error obteniendo mascotas del dueño: {e}")
        return []

def buscar_mascota_por_nombre(nombre):
    """Buscar mascotas por nombre"""
    try:
        resultado = supabase.table("mascota").select("*, dueno(nombre, telefono)").ilike("nombre", f"%{nombre}%").execute()
        return resultado.data
    except Exception as e:
        print(f"Error buscando mascota: {e}")
        return []

# ========== OPERACIONES PARA VETERINARIOS ==========
def crear_veterinario(nombre, especialidad, telefono, email):
    """Crear nuevo veterinario"""
    try:
        datos = {
            "nombre": nombre,
            "especialidad": especialidad,
            "telefono": telefono,
            "email": email
        }
        resultado = supabase.table("veterinario").insert(datos).execute()
        if resultado.data:
            print(f"Veterinario '{nombre}' creado con ID: {resultado.data[0]['id_veterinario']}")
            return resultado.data[0]['id_veterinario']
        return None
    except Exception as e:
        print(f"Error creando veterinario: {e}")
        return None

def obtener_veterinarios():
    """Obtener todos los veterinarios"""
    try:
        resultado = supabase.table("veterinario").select("*").order("id_veterinario").execute()
        return resultado.data
    except Exception as e:
        print(f"Error obteniendo veterinarios: {e}")
        return []

# ========== OPERACIONES PARA CONSULTAS ==========
def crear_consulta(motivo, diagnostico, tratamiento, observaciones, id_mascota, id_veterinario=None):
    """Crear nueva consulta médica"""
    try:
        datos = {
            "motivo": motivo,
            "diagnostico": diagnostico,
            "tratamiento": tratamiento,
            "observaciones": observaciones,
            "id_mascota": id_mascota,
            "id_veterinario": id_veterinario
        }
        resultado = supabase.table("consulta").insert(datos).execute()
        if resultado.data:
            print(f"✅ Consulta creada con ID: {resultado.data[0]['id_consulta']}")
            return resultado.data[0]['id_consulta']
        return None
    except Exception as e:
        print(f"Error creando consulta: {e}")
        return None

def obtener_consultas_por_mascota(id_mascota):
    """Obtener historial de consultas de una mascota"""
    try:
        resultado = supabase.table("consulta").select("*, veterinario(nombre, especialidad)").eq("id_mascota", id_mascota).order("fecha_consulta", desc=True).execute()
        return resultado.data
    except Exception as e:
        print(f"Error obteniendo consultas: {e}")
        return []

def obtener_todas_consultas():
    """Obtener todas las consultas con información relacionada"""
    try:
        resultado = supabase.table("consulta").select("*, mascota(nombre, especie), veterinario(nombre)").order("fecha_consulta", desc=True).execute()
        return resultado.data
    except Exception as e:
        print(f"Error obteniendo consultas: {e}")
        return []

# ========== REPORTES ESPECIALES ==========
def reporte_historial_completo(id_mascota):
    """Generar reporte completo del historial clínico"""
    try:
        # Obtener información de la mascota y dueño
        mascota_info = supabase.table("mascota").select("*, dueno(*)").eq("id_mascota", id_mascota).execute()
        
        if not mascota_info.data:
            print("Mascota no encontrada")
            return None
        
        mascota = mascota_info.data[0]
        dueno = mascota['dueno']
        
        # Obtener historial de consultas
        consultas = obtener_consultas_por_mascota(id_mascota)
        
        return {
            "mascota": mascota,
            "dueno": dueno,
            "consultas": consultas
        }
        
    except Exception as e:
        print(f"Error generando reporte: {e}")
        return None

def estadisticas_veterinaria():
    """Estadísticas generales de la veterinaria"""
    try:
        # Contar dueños
        dueños_count = len(obtener_duenos())
        
        # Contar mascotas
        mascotas_count = len(obtener_mascotas())
        
        # Contar veterinarios
        veterinarios_count = len(obtener_veterinarios())
        
        # Contar consultas
        consultas_count = len(obtener_todas_consultas())
        
        return {
            "total_dueños": dueños_count,
            "total_mascotas": mascotas_count,
            "total_veterinarios": veterinarios_count,
            "total_consultas": consultas_count
        }
        
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return {}

# ========== EJEMPLOS DE USO ==========
def ejemplos_practicos():
    """Ejemplos de cómo usar las funciones"""
    print("🚀 Ejemplos prácticos de uso:")
    
    # 1. Crear un dueño
    # id_dueno = crear_dueno("Carlos López", "Calle 123", "555-0001", "carlos@email.com")
    
    # 2. Crear una mascota para ese dueño
    # id_mascota = crear_mascota("Max", "Perro", "Labrador", "2020-05-15", id_dueno)
    
    # 3. Crear un veterinario
    # id_veterinario = crear_veterinario("Dra. Ana García", "Cirugía", "555-0002", "ana@vet.com")
    
    # 4. Crear una consulta
    # crear_consulta("Control anual", "Saludable", "Vacuna anual", "Mascota en buen estado", id_mascota, id_veterinario)
    
    # 5. Buscar mascotas por nombre
    # mascotas = buscar_mascota_por_nombre("Max")
    
    # 6. Generar reporte completo
    # reporte = reporte_historial_completo(1)
    
    # 7. Ver estadísticas
    # stats = estadisticas_veterinaria()
    # print(f"Estadísticas: {stats}")
    
    pass

if __name__ == "__main__":
    # Probar conexión y funciones básicas
    try:
        print("🔍 Probando conexión y obteniendo datos...")
        
        dueños = obtener_duenos()
        print(f"📊 Dueños en sistema: {len(dueños)}")
        
        mascotas = obtener_mascotas()
        print(f"🐕 Mascotas en sistema: {len(mascotas)}")
        
        veterinarios = obtener_veterinarios()
        print(f"👨‍⚕️ Veterinarios en sistema: {len(veterinarios)}")
        
        consultas = obtener_todas_consultas()
        print(f"📋 Consultas en sistema: {len(consultas)}")
        
    except Exception as e:
        print(f"Error en pruebas: {e}")