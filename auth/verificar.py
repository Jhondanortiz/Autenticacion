import os
import sys

def print_header(text):
    """Imprime un encabezado decorado"""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70)

def check_file(filepath, description):
    """Verifica si un archivo existe"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description:40} {filepath}")
    return exists

def check_directory(dirpath, description):
    """Verifica si un directorio existe"""
    exists = os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {description:40} {dirpath}")
    return exists

def check_file_content(filepath, search_text):
    """Verifica si un archivo contiene cierto texto"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return search_text in content
    except:
        return False

def main():
    """Función principal de verificación"""
    
    print_header("🔍 VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO SECURELINK")
    
    all_ok = True
    
    # ========================================================================
    # VERIFICAR ARCHIVOS PRINCIPALES
    # ========================================================================
    print_header("📄 ARCHIVOS PRINCIPALES")
    
    files_main = [
        ("app.py", "Código principal de Flask"),
        ("requirements.txt", "Dependencias de Python"),
        ("README.md", "Documentación del proyecto"),
    ]
    
    for filename, description in files_main:
        if not check_file(filename, description):
            all_ok = False
    
    # ========================================================================
    # VERIFICAR CARPETAS
    # ========================================================================
    print_header("📁 ESTRUCTURA DE CARPETAS")
    
    directories = [
        ("templates", "Plantillas HTML"),
        ("static", "Archivos estáticos"),
        ("static/css", "Hojas de estilo"),
        ("static/js", "Scripts JavaScript"),
    ]
    
    for dirpath, description in directories:
        if not check_directory(dirpath, description):
            all_ok = False
    
    # ========================================================================
    # VERIFICAR TEMPLATES HTML
    # ========================================================================
    print_header("🌐 TEMPLATES HTML")
    
    templates = [
        ("templates/base.html", "Plantilla base"),
        ("templates/login.html", "Página de login"),
        ("templates/registro.html", "Página de registro"),
        ("templates/admin.html", "Panel de administración"),
        ("templates/user.html", "Panel de usuario"),
        ("templates/guest.html", "Panel de invitado"),
        ("templates/perfil.html", "Perfil de usuario"),
    ]
    
    for filepath, description in templates:
        if not check_file(filepath, description):
            all_ok = False
    
    # ========================================================================
    # VERIFICAR CSS
    # ========================================================================
    print_header("🎨 ARCHIVOS CSS")
    
    css_files = [
        ("static/css/custom.css", "Estilos personalizados"),
    ]
    
    for filepath, description in css_files:
        if not check_file(filepath, description):
            all_ok = False
    
    # ========================================================================
    # VERIFICAR CONTENIDO CRÍTICO
    # ========================================================================
    print_header("🔍 VERIFICACIÓN DE CONTENIDO")
    
    checks = []
    
    # Verificar app.py
    if os.path.exists("app.py"):
        has_bcrypt = check_file_content("app.py", "bcrypt")
        has_flask = check_file_content("app.py", "Flask")
        has_login = check_file_content("app.py", "@app.route('/login'")
        has_registro = check_file_content("app.py", "@app.route('/registro'")
        
        checks.append(("app.py usa bcrypt", has_bcrypt))
        checks.append(("app.py usa Flask", has_flask))
        checks.append(("app.py tiene ruta /login", has_login))
        checks.append(("app.py tiene ruta /registro", has_registro))
    
    # Verificar base.html
    if os.path.exists("templates/base.html"):
        has_css_link = check_file_content("templates/base.html", "custom.css")
        has_bootstrap = check_file_content("templates/base.html", "bootstrap")
        
        checks.append(("base.html carga custom.css", has_css_link))
        checks.append(("base.html carga Bootstrap", has_bootstrap))
    
    # Verificar registro.html
    if os.path.exists("templates/registro.html"):
        has_rol_selection = check_file_content("templates/registro.html", 'name="rol"')
        
        checks.append(("registro.html tiene selección de rol", has_rol_selection))
    
    # Verificar custom.css
    if os.path.exists("static/css/custom.css"):
        has_variables = check_file_content("static/css/custom.css", ":root")
        has_gradient = check_file_content("static/css/custom.css", "gradient")
        
        checks.append(("custom.css tiene variables CSS", has_variables))
        checks.append(("custom.css tiene gradientes", has_gradient))
    
    for description, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {description}")
        if not passed:
            all_ok = False
    
    # ========================================================================
    # VERIFICAR DEPENDENCIAS
    # ========================================================================
    print_header("📦 VERIFICACIÓN DE DEPENDENCIAS")
    
    try:
        import flask
        print(f"✅ Flask instalado (versión {flask.__version__})")
    except ImportError:
        print("❌ Flask NO está instalado")
        all_ok = False
    
    try:
        import bcrypt
        print(f"✅ bcrypt instalado")
    except ImportError:
        print("❌ bcrypt NO está instalado")
        all_ok = False
    
    # ========================================================================
    # VERIFICAR BASE DE DATOS
    # ========================================================================
    print_header("🗄️ BASE DE DATOS")
    
    if os.path.exists("securelink.db"):
        print("✅ Base de datos existe: securelink.db")
        
        # Intentar verificar la estructura
        try:
            import sqlite3
            conn = sqlite3.connect("securelink.db")
            cursor = conn.cursor()
            
            # Verificar tabla usuarios
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
            if cursor.fetchone():
                print("✅ Tabla 'usuarios' existe")
                
                # Contar usuarios
                cursor.execute("SELECT COUNT(*) FROM usuarios")
                count = cursor.fetchone()[0]
                print(f"✅ Usuarios registrados: {count}")
            else:
                print("❌ Tabla 'usuarios' NO existe")
                all_ok = False
            
            conn.close()
        except Exception as e:
            print(f"⚠️  Error al verificar base de datos: {e}")
    else:
        print("⚠️  Base de datos NO existe (se creará al ejecutar app.py)")
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print_header("📊 RESUMEN FINAL")
    
    if all_ok:
        print("""
✅ ¡TODO ESTÁ CORRECTO!

Tu proyecto está correctamente estructurado y listo para ejecutar.

🚀 PRÓXIMOS PASOS:

1. Instalar dependencias (si no lo has hecho):
   pip install -r requirements.txt

2. Ejecutar la aplicación:
   python app.py

3. Abrir el navegador en:
   http://127.0.0.1:5000

4. Iniciar sesión con:
   Usuario: admin
   Contraseña: Admin123!
        """)
    else:
        print("""
❌ HAY PROBLEMAS EN LA ESTRUCTURA

Revisa los elementos marcados con ❌ arriba.

💡 SOLUCIONES COMUNES:

1. Archivos faltantes:
   - Asegúrate de copiar todos los códigos
   - Verifica los nombres de archivos (case sensitive)

2. Carpetas faltantes:
   mkdir templates static static/css static/js

3. Dependencias faltantes:
   pip install -r requirements.txt

4. CSS no carga:
   - Verifica que custom.css esté en static/css/
   - Verifica que base.html tenga la línea:
     <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
        """)
    
    print("="*70)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())