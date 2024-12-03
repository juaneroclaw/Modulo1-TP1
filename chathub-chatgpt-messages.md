**user**: quiero correr python3 -m venv venv y me arroja el siguiente error: No se encontr¾ Python; ejecuta sin argumentos para instalar desde Microsoft Store o deshabilita este acceso directo en Configuraci¾n > Administrar alias de ejecuci¾n de la aplicaci¾n. Aclaro que ya instale winget install Python.Python.3.11
**chatgpt**: El error indica que tu sistema no encuentra el comando `python` o `python3` a pesar de que has instalado Python usando `winget`. Esto podría deberse a que la instalación no configuró correctamente las variables de entorno o los alias de ejecución en tu sistema. Aquí tienes algunos pasos para solucionar el problema:

---

### 1. **Verifica la Instalación de Python**
Confirma que Python está instalado correctamente en tu sistema:
- Abre una terminal (CMD o PowerShell).
- Escribe `winget list` para verificar si `Python.Python.3.11` aparece en la lista.
- Si aparece, intenta ejecutar el comando `python --version` o `python3 --version`.

---

### 2. **Configura el Alias de Ejecución (Run Alias)**
Windows puede estar redirigiendo `python` a la Microsoft Store. Para corregirlo:
- Abre Configuración (Windows + I).
- Ve a **Aplicaciones** > **Aplicaciones predeterminadas** > **Administrar alias de ejecución**.
- Busca `python` o `python3` y asegúrate de que el alias esté habilitado para la instalación correcta de Python.

---

### 3. **Agrega Python a las Variables de Entorno**
Es posible que Python no esté en el PATH del sistema. Para solucionarlo:
1. Encuentra la ruta de instalación de Python:
   - Generalmente, está en `C:\Users\<tu_usuario>\AppData\Local\Programs\Python\Python311\` o una ruta similar.
2. Agrega estas rutas a las variables de entorno:
   - Ve a **Panel de control** > **Sistema** > **Configuración avanzada del sistema** > **Variables de entorno**.
   - En la sección **Variables del sistema**, selecciona `Path` y haz clic en **Editar**.
   - Agrega estas dos rutas:
     - La carpeta principal de Python (`C:\...\Python311\`).
     - La carpeta `Scripts` dentro de la instalación de Python (`C:\...\Python311\Scripts\`).

---

### 4. **Usa Comandos Completos**
Si los pasos anteriores no funcionan, puedes usar el camino completo al ejecutar comandos:
```bash
C:\Users\<tu_usuario>\AppData\Local\Programs\Python\Python311\python.exe -m venv venv
```

---

### 5. **Reinstala Python (Si Necesario)**
Si sigue sin funcionar, reinstala Python asegurándote de marcar la opción **Add Python to PATH** durante la instalación manual desde [python.org](https://www.python.org/downloads/).

---

### Prueba Final
Después de realizar estos pasos, reinicia la terminal y ejecuta nuevamente:
```bash
python -m venv venv
```

¿Funcionó? 😊