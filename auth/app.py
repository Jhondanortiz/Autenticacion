from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
from functools import wraps
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'securelink_clave_ultra_secreta_2024_bcrypt'

DATABASE = 'securelink.db'

# ============================================================================
# FUNCIONES DE BASE DE DATOS
# ============================================================================

def get_db_connection():
    """Establece conexión con la base de datos SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos y crea usuarios de ejemplo"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('admin', 'usuario', 'invitado')),
            nombre_completo TEXT NOT NULL,
            email TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acceso TIMESTAMP,
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Verificar si ya existen usuarios
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("\n" + "="*70)
        print("🔧 Creando usuarios iniciales...")
        print("="*70)
        
        # Crear usuarios de ejemplo
        usuarios_iniciales = [
            {
                'username': 'admin',
                'password': 'Admin123!',
                'rol': 'admin',
                'nombre': 'Administrador del Sistema',
                'email': 'admin@securelink.com'
            },
            {
                'username': 'juan.perez',
                'password': 'Usuario123!',
                'rol': 'usuario',
                'nombre': 'Juan Pérez García',
                'email': 'juan.perez@securelink.com'
            },
            {
                'username': 'maria.lopez',
                'password': 'Usuario123!',
                'rol': 'usuario',
                'nombre': 'María López Rodríguez',
                'email': 'maria.lopez@securelink.com'
            },
            {
                'username': 'invitado',
                'password': 'Invitado123!',
                'rol': 'invitado',
                'nombre': 'Usuario Invitado',
                'email': 'invitado@securelink.com'
            }
        ]
        
        for user in usuarios_iniciales:
            password_hash = hash_password(user['password'])
            cursor.execute('''
                INSERT INTO usuarios (username, password_hash, rol, nombre_completo, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (user['username'], password_hash, user['rol'], user['nombre'], user['email']))
            print(f"✅ Usuario creado: {user['username']} ({user['rol']})")
        
        conn.commit()
        
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("="*70)
        for user in usuarios_iniciales:
            print(f"👤 {user['rol'].upper():10} | Usuario: {user['username']:15} | Password: {user['password']}")
        print("="*70 + "\n")
    else:
        print(f"\n✅ Base de datos encontrada con {count} usuarios")
    
    conn.close()

def actualizar_ultimo_acceso(user_id):
    """Actualiza la fecha del último acceso del usuario"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios 
        SET ultimo_acceso = CURRENT_TIMESTAMP 
        WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

# ============================================================================
# FUNCIONES CRIPTOGRÁFICAS CON BCRYPT
# ============================================================================

def hash_password(password):
    """
    Genera un hash seguro de la contraseña usando bcrypt
    
    bcrypt características:
    - Salt automático único por contraseña
    - Cost factor = 12 (4,096 iteraciones)
    - Tiempo aprox: 250ms (previene fuerza bruta)
    - Formato: $2b$12$[22 chars salt][31 chars hash]
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password_bytes, salt)
    return password_hash.decode('utf-8')

def verify_password(password, password_hash):
    """
    Verifica si una contraseña coincide con su hash
    
    Seguridad:
    - Comparación en tiempo constante (previene timing attacks)
    - El salt se extrae automáticamente del hash
    """
    try:
        password_bytes = password.encode('utf-8')
        password_hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)
    except Exception as e:
        print(f"Error al verificar password: {e}")
        return False

# ============================================================================
# DECORADORES DE PROTECCIÓN DE RUTAS
# ============================================================================

def login_required(f):
    """
    Decorador que protege rutas requiriendo autenticación
    Si el usuario no está autenticado, redirige al login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('⚠️ Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    """
    Decorador que protege rutas por rol
    roles: lista de roles permitidos, ej: ['admin', 'usuario']
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('⚠️ Debes iniciar sesión', 'warning')
                return redirect(url_for('login'))
            
            if session.get('rol') not in roles:
                flash('❌ No tienes permisos para acceder a esta página', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================================================
# RUTAS PÚBLICAS (sin autenticación requerida)
# ============================================================================

@app.route('/')
def index():
    """Página principal - Redirige según estado de sesión"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    
    # Si ya está logueado, redirigir
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validar campos
        if not username or not password:
            flash('⚠️ Por favor completa todos los campos', 'danger')
            return render_template('login.html')
        
        # Buscar usuario en la base de datos
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM usuarios WHERE username = ? AND activo = 1', 
            (username,)
        ).fetchone()
        conn.close()
        
        # Verificar credenciales
        if user and verify_password(password, user['password_hash']):
            # ✅ Credenciales correctas - Crear sesión
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['rol'] = user['rol']
            session['nombre'] = user['nombre_completo']
            session['email'] = user['email']
            
            # Actualizar último acceso
            actualizar_ultimo_acceso(user['id'])
            
            flash(f'🎉 ¡Bienvenido {user["nombre_completo"]}!', 'success')
            
            # Redirigir según rol
            if user['rol'] == 'admin':
                return redirect(url_for('admin_panel'))
            elif user['rol'] == 'usuario':
                return redirect(url_for('user_panel'))
            elif user['rol'] == 'invitado':
                return redirect(url_for('guest_panel'))
            else:
                return redirect(url_for('dashboard'))
        else:
            # ❌ Credenciales incorrectas
            flash('❌ Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios CON SELECCIÓN DE ROL"""
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        nombre_completo = request.form.get('nombre_completo', '').strip()
        email = request.form.get('email', '').strip()
        rol = request.form.get('rol', 'usuario')  # ← NUEVO: selección de rol
        
        # Validaciones
        if not all([username, password, password_confirm, nombre_completo, email, rol]):
            flash('⚠️ Por favor completa todos los campos', 'danger')
            return render_template('registro.html')
        
        if password != password_confirm:
            flash('⚠️ Las contraseñas no coinciden', 'danger')
            return render_template('registro.html')
        
        if len(password) < 8:
            flash('⚠️ La contraseña debe tener al menos 8 caracteres', 'danger')
            return render_template('registro.html')
        
        if rol not in ['admin', 'usuario', 'invitado']:
            flash('⚠️ Rol inválido', 'danger')
            return render_template('registro.html')
        
        # Verificar si el usuario ya existe
        conn = get_db_connection()
        existing_user = conn.execute(
            'SELECT * FROM usuarios WHERE username = ?', 
            (username,)
        ).fetchone()
        
        if existing_user:
            conn.close()
            flash('⚠️ El nombre de usuario ya está en uso', 'danger')
            return render_template('registro.html')
        
        # Crear nuevo usuario
        password_hash = hash_password(password)
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (username, password_hash, rol, nombre_completo, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, rol, nombre_completo, email))
            conn.commit()
            
            user_id = cursor.lastrowid
            conn.close()
            
            print(f"\n✅ Nuevo usuario registrado:")
            print(f"   ID: {user_id}")
            print(f"   Usuario: {username}")
            print(f"   Rol: {rol}")
            print(f"   Email: {email}\n")
            
            flash(f'✅ Registro exitoso como {rol}. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            conn.close()
            flash(f'❌ Error al registrar usuario: {str(e)}', 'danger')
            print(f"Error en registro: {e}")
    
    return render_template('registro.html')

# ============================================================================
# RUTAS PROTEGIDAS (requieren autenticación)
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard general - Redirige según rol"""
    rol = session.get('rol')
    
    if rol == 'admin':
        return redirect(url_for('admin_panel'))
    elif rol == 'usuario':
        return redirect(url_for('user_panel'))
    elif rol == 'invitado':
        return redirect(url_for('guest_panel'))
    
    return render_template('dashboard.html')

@app.route('/admin')
@role_required(['admin'])
def admin_panel():
    """Panel de administración - Solo para admins"""
    conn = get_db_connection()
    usuarios = conn.execute('''
        SELECT * FROM usuarios 
        ORDER BY fecha_creacion DESC
    ''').fetchall()
    
    # Estadísticas
    stats = {
        'total': len(usuarios),
        'admins': len([u for u in usuarios if u['rol'] == 'admin']),
        'usuarios': len([u for u in usuarios if u['rol'] == 'usuario']),
        'invitados': len([u for u in usuarios if u['rol'] == 'invitado']),
        'activos': len([u for u in usuarios if u['activo'] == 1])
    }
    
    conn.close()
    
    return render_template('admin.html', usuarios=usuarios, stats=stats)

@app.route('/user')
@role_required(['usuario', 'admin'])
def user_panel():
    """Panel de usuario - Para usuarios normales"""
    return render_template('user.html')

@app.route('/guest')
@role_required(['invitado', 'admin'])
def guest_panel():
    """Panel de invitado - Acceso limitado"""
    return render_template('guest.html')

@app.route('/perfil')
@login_required
def perfil():
    """Página de perfil del usuario"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM usuarios WHERE id = ?', 
        (session['user_id'],)
    ).fetchone()
    conn.close()
    
    if not user:
        flash('❌ Usuario no encontrado', 'danger')
        return redirect(url_for('logout'))
    
    return render_template('perfil.html', user=user)

# ============================================================================
# GESTIÓN DE USUARIOS (Solo Admin)
# ============================================================================

@app.route('/admin/usuarios')
@role_required(['admin'])
def admin_usuarios():
    """Administración de usuarios"""
    conn = get_db_connection()
    usuarios = conn.execute('''
        SELECT * FROM usuarios 
        ORDER BY fecha_creacion DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin_usuarios.html', usuarios=usuarios)

# ============================================================================
# CERRAR SESIÓN
# ============================================================================

@app.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    nombre = session.get('nombre', 'Usuario')
    session.clear()
    flash(f'👋 Hasta luego, {nombre}. Has cerrado sesión correctamente', 'info')
    return redirect(url_for('login'))

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ============================================================================
# INICIALIZACIÓN Y EJECUCIÓN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🔐 SECURELINK - Sistema de Autenticación con bcrypt")
    print("="*70)
    
    # Inicializar base de datos
    init_db()
    
    print("\n🌐 SERVIDOR INICIADO")
    print("="*70)
    print(f"📍 URL: http://127.0.0.1:5000")
    print(f"📍 URL Local: http://localhost:5000")
    print(f"🔐 Algoritmo: bcrypt (rounds=12)")
    print(f"💾 Base de datos: {DATABASE}")
    print("="*70)
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    
    # Iniciar servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)