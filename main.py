"""
API REST con autenticación JWT y operaciones sobre listas numéricas.

Este módulo implementa una API con FastAPI que incluye:
- Sistema de autenticación con JWT
- Operaciones matemáticas y de ordenamiento
- Validación de datos con Pydantic
"""

from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

# Configuración inicial
app = FastAPI()
fake_db = {"users": {}}
SECRET_KEY = "tu_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Modelos Pydantic
class UserRegister(BaseModel):
    """
    Modelo para registro de usuarios.
    
    Attributes:
        username (str): Nombre de usuario
        password (str): Contraseña del usuario
    """
    username: str
    password: str

class UserLogin(BaseModel):
    """
    Modelo para inicio de sesión.
    
    Attributes:
        username (str): Nombre de usuario
        password (str): Contraseña del usuario
    """
    username: str
    password: str

class Payload(BaseModel):
    """
    Modelo para operaciones con listas numéricas.
    
    Attributes:
        numbers (List[int]): Lista de números enteros
    """
    numbers: List[int]

class BinarySearchPayload(BaseModel):
    """
    Modelo para búsqueda binaria.
    
    Attributes:
        numbers (List[int]): Lista ordenada de números enteros
        target (int): Número a buscar
    """
    numbers: List[int]
    target: int
# generar un token JWT con algoritmo HS256. Este token debe incluirse como un parámetro de consulta (query parameter) llamado token en cada solicitud a los endpoints protegidos. El token sirve como tu credencial de autenticación, permitiendo que el sistema verifique tu identidad y autorice tu acceso a los recursos solicitados.

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funciones de utilidad
def create_access_token(data: dict) -> str:
    """
    Genera un token JWT para autenticación.
    
    Args:
        data (dict): Datos a codificar en el token
    
    Returns:
        str: Token JWT generado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# Implementa un endpoint para la creación de usuarios y otro para el inicio de sesión. Los usuarios deben autenticarse para poder acceder a los endpoints existentes.
# Ruta Registro: /register
# Método: POST
# Entrada (Body): {"username": "user1", "password": "pass1"}
# Salida: {"message": "User registered successfully"}
# Status Code:
# 200: Registro exitoso
# 400: El usuario ya existe

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        plain_password (str): Contraseña en texto plano
        hashed_password (str): Hash almacenado
    
    Returns:
        bool: True si coinciden, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Genera hash de contraseña usando bcrypt.
    
    Args:
        password (str): Contraseña en texto plano
    
    Returns:
        str: Hash de la contraseña
    """
    return pwd_context.hash(password)

def get_current_user(token: str) -> str:
    """
    Valida token JWT y retorna usuario.
    
    Args:
        token (str): Token JWT a validar
    
    Returns:
        str: Username del token
        
    Raises:
        HTTPException: Si el token es inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Endpoints de autenticación
@app.post("/register", status_code=200)
async def register(user: UserRegister):
    """
    Registra un nuevo usuario.
    
    Args:
        user (UserRegister): Datos del usuario
    
    Returns:
        dict: Mensaje de éxito
        
    Raises:
        HTTPException: Si el usuario ya existe
    """
    if user.username in fake_db["users"]:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(user.password)
    fake_db["users"][user.username] = {"password": hashed_password}
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserLogin):
    """
    Inicia sesión y genera token JWT.
    
    Args:
        user (UserLogin): Credenciales de usuario
    
    Returns:
        dict: Token de acceso
        
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    if user.username not in fake_db["users"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    stored_user = fake_db["users"][user.username]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token}

# Utiliza CryptContext de passlib para cifrar las contraseñas antes de guardarlas en tu base de datos simulada (fake_db).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)



# Bubble Sort
# Ruta: /bubble-sort
# Método: POST
# Descripción: Recibe una lista de números y devuelve la lista ordenada utilizando el algoritmo de Bubble Sort.
# Entrada: {"numbers": [lista de números]}
# Salida: {"numbers": [lista de números ordenada]}


from jwt.exceptions import InvalidTokenError

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.post("/bubble-sort")
def bubble_sort(payload: Payload, token: str):
    """
    Ordena lista usando bubble sort.
    
    Args:
        payload (Payload): Lista a ordenar
        token (str): Token JWT
    
    Returns:
        dict: Lista ordenada
    """
    get_current_user(token)
    numbers = payload.numbers
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return {"numbers": numbers}

# Filtro de Pares
# Ruta: /filter-even
# Método: POST
# Descripción: Recibe una lista de números y devuelve únicamente aquellos que son pares.
# Entrada: {"numbers": [lista de números]}
# Salida: {"even_numbers": [lista de números pares]}

@app.post("/filter-even")
def filter_even(payload: Payload, token: str):
    """
    Filtra números pares de una lista.
    
    Args:
        payload (Payload): Lista de números
        token (str): Token JWT
    
    Returns:
        dict: Lista de números pares
    """
    get_current_user(token)
    numbers = payload.numbers
    even_numbers = [number for number in numbers if number % 2 == 0]
    return {"even_numbers": even_numbers}

# Suma de Elementos
# Ruta: /sum-elements
# Método: POST
# Descripción: Recibe una lista de números y devuelve la suma de sus elementos.
# Entrada: {"numbers": [lista de números]}
# Salida: {"sum": suma de los números}
@app.post("/sum-elements")
def sum_elements(payload: Payload, token: str):
    """
    Suma elementos de una lista.
    
    Args:
        payload (Payload): Lista de números
        token (str): Token JWT
    
    Returns:
        dict: Suma total
    """
    get_current_user(token)
    numbers = payload.numbers
    return {"sum": sum(numbers)}


# Máximo Valor
# Ruta: /max-value
# Método: POST
# Descripción: Recibe una lista de números y devuelve el valor máximo.
# Entrada: {"numbers": [lista de números]}
# Salida: {"max": número máximo}
@app.post("/max-value")
def max_value(payload: Payload, token: str):
    """
    Encuentra el valor máximo.
    
    Args:
        payload (Payload): Lista de números
        token (str): Token JWT
    
    Returns:
        dict: Valor máximo
    """
    get_current_user(token)
    numbers = payload.numbers
    return {"max": max(numbers)}

# Busqueda Binaria
# Ruta: /binary-search
# Método: POST
# Descripción: Recibe una lista de números ordenada y un número objetivo, y devuelve la posición del número objetivo en la lista utilizando el algoritmo de búsqueda binaria.
# Entrada: {"numbers": [lista de números ordenada], "target": número objetivo}
# Salida
    # 1. Si el número objetivo está en la lista, devuelve la posición del número objetivo.
    # 2. Si el número objetivo no está en la lista, devuelve -1.
@app.post("/binary-search")
def binary_search(payload: BinarySearchPayload, token: str):
    """
    Realiza búsqueda binaria.
    
    Args:
        payload (BinarySearchPayload): Lista ordenada y valor objetivo
        token (str): Token JWT
    
    Returns:
        dict: Estado de búsqueda y posición
    """
    get_current_user(token)
    numbers = payload.numbers
    target = payload.target
    
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            return {"found": True, "index": mid}
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return {"found": False, "index": -1}