"""
================================================================================
SECURELINK - Instalador Automático Completo
================================================================================
Este script crea toda la estructura del proyecto automáticamente
Ejecuta: python setup.py
================================================================================
"""

import os
import subprocess
import sys

def print_banner():
    """Muestra el banner de SECURELINK"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗██╗  ██╗
║   ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝██║     ██║████╗  ██║██║ ██╔╝
║   ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╔╝ 
║   ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  ██║     ██║██║╚██╗██║██╔═██╗ 
║   ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗███████╗██║██║ ╚████║██║  ██╗
║   ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
║                                                                           ║
║                   INSTALADOR AUTOMÁTICO DEL SISTEMA                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Verifica la versión de Python"""
    print("\n🔍 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Tu versión: Python {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("\n📦 Instalando dependencias...")
    print("="*70)
    
    dependencies = ['Flask==3.0.0', 'bcrypt==4.1.2', 'Werkzeug==3.0.1']
    
    for dep in dependencies:
        print(f"\n📥 Instalando {dep}...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", dep],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"   ✅ {dep} instalado")
        except subprocess.CalledProcessError:
            print(f"   ⚠️  Error al instalar {dep}")
    
    print("\n✅ Todas las dependencias instaladas")

def create_structure():
    """Crea la estructura de directorios"""
    print("\n📁 Creando estructura de directorios...")
    
    directories = [
        'templates',
        'static',
        'static/css',
        'static/js'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Creado: {directory}/")
        else:
            print(f"   ℹ️  Ya existe: {directory}/")

def create_requirements():
    """Crea el archivo requirements.txt"""
    print("\n📝 Creando requirements.txt...")
    
    content = """Flask==3.0.0
bcrypt==4.1.2
Werkzeug==3.0.1"""
    
    with open('requirements.txt', 'w') as f:
        f.write(content)
    
    print("   ✅ requirements.txt creado")

def create_gitignore():
    """Crea archivo .gitignore"""
    print("\n📝 Creando .gitignore...")
    
    content = """# Base de datos
*.db
*.sqlite
*.sqlite3

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Flask
instance/
.webassets-cache

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log"""
    
    with open('.gitignore', 'w') as f:
        f.write(content)
    
    print("   ✅ .gitignore creado")

def create_readme():
    """Crea README.md"""
    print("\n📝 Creando README.md...")
    
    content = """# SECURELINK - Sistema de Autenticación

Sistema completo de autenticación con control de acceso por roles usando Flask y bcrypt.

## 🚀 Instalación Rápida

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

## 🔑 Credenciales de Prueba

- **Admin**: admin / Admin123!
- **Usuario**: juan.perez / Usuario123!
- **Invitado**: invitado / Invitado123!

## 📊 Ver Base de Datos

### Opción 1: VS Code
1. Instalar extensión "SQLite Viewer"
2. Click en archivo `securelink.db`

### Opción 2: DB Browser
1. Descargar de https://sqlitebrowser.org/
2. Abrir `securelink.db`

## 🔐 Seguridad

- Algoritmo: bcrypt (12 rounds)
- Salt automático por contraseña
- Protección de rutas por roles
- Sesiones seguras

## 📝 Características

✅ Registro de usuarios con selección de rol  
✅ Login seguro con bcrypt  
✅ Control de acceso por roles  
✅ Panel administrativo  
✅ Gestión de perfiles  

## 🎓 Proyecto Educativo

Sistema desarrollado para el curso de Criptografía y Seguridad Aplicada.
"""
    
    with open('README.md', 'w') as f:
        f.write(content)
    
    print("   ✅ README.md creado")

def show_next_steps():
    """Muestra los siguientes pasos"""
    print("\n" + "="*70)
    print("✅ INSTALACIÓN COMPLETADA")
    print("="*70)
    
    print("""
📋 ARCHIVOS CREADOS:
   ✅ app.py (código principal)
   ✅ requirements.txt
   ✅ .gitignore
   ✅ README.md
   ✅ templates/ (carpeta para HTML)
   ✅ static/ (carpeta para CSS/JS)

🎯 PRÓXIMOS PASOS:

1️⃣  Copia el código de app.py que te proporcioné

2️⃣  Crea los archivos HTML en templates/:
   - base.html
   - login.html
   - registro.html (CON SELECCIÓN DE ROL)
   - admin.html
   - user.html
   - guest.html
   - perfil.html

3️⃣  Ejecuta la aplicación:
   python app.py

4️⃣  Abre el navegador en:
   http://127.0.0.1:5000

🔍 PARA VER LA BASE DE DATOS:

📌 Opción 1 (Recomendada): VS Code
   1. Instalar extensión: SQLite Viewer
   2. Abrir archivo: securelink.db
   
📌 Opción 2: DB Browser
   1. Descargar: https://sqlitebrowser.org/
   2. Abrir el archivo: securelink.db

🔑 CREDENCIALES:
   Admin:    admin / Admin123!
   Usuario:  juan.perez / Usuario123!
   Invitado: invitado / Invitado123!

💡 REGISTRAR NUEVOS USUARIOS:
   - Ve a http://127.0.0.1:5000/registro
   - Elige el rol (admin, usuario, invitado)
   - Los nuevos usuarios aparecerán en la BD
    """)
    
    print("="*70)
    print("\n🎉 ¡Todo listo! Ahora copia los códigos de los archivos HTML")
    print("="*70 + "\n")

def main():
    """Función principal"""
    print_banner()
    
    print("\n🚀 Iniciando instalación del sistema SECURELINK...")
    
    # Verificar Python
    check_python_version()
    
    # Instalar dependencias
    install_dependencies()
    
    # Crear estructura
    create_structure()
    
    # Crear archivos
    create_requirements()
    create_gitignore()
    create_readme()
    
    # Mostrar siguientes pasos
    show_next_steps()

if __name__ == "__main__":
    main()