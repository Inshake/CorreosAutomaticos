// --- Selección de elementos ---
const form = document.getElementById("envioForm");
const toast = document.getElementById("toast");
const modal = document.getElementById("confirmModal");
const confirmYes = document.getElementById("confirmYes");
const confirmNo = document.getElementById("confirmNo");
const btnEnviar = document.getElementById("btnEnviar");
const btnLimpiar = document.getElementById("btnLimpiar");
const archivo = document.getElementById("archivo");


// Función para mostrar mensajes (toast)
function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}


// --- VALIDACIONES ---
function validarFormulario() {
    let valido = true;

    // Limpia errores anteriores
    document.querySelectorAll(".error").forEach(e => e.classList.remove("error"));

    const asunto = document.getElementById("asunto");
    const texto = document.getElementById("texto");
    const correo = document.getElementById("correo");
    const pass = document.getElementById("contraseniaSec");
    const archivo = document.getElementById("archivo");

    // CHECK 1: Campos vacíos
    if (!asunto.value.trim()) { asunto.classList.add("error"); valido = false; }
    if (!texto.value.trim()) { texto.classList.add("error"); valido = false; }
    if (!correo.value.trim()) { correo.classList.add("error"); valido = false; }
    if (!pass.value.trim()) { pass.classList.add("error"); valido = false; }

    // CHECK 2: Validar extensión del archivo
    if (!archivo.value.endsWith(".xlsx") && !archivo.value.endsWith(".xls")) {
        archivo.classList.add("error");
        valido = false;
        showToast("El archivo debe ser Excel (.xlsx o .xls)");
    }

    return valido;
}


// --- Interceptar envío ---
form.addEventListener("submit", function (e) {
    e.preventDefault();  // detiene el submit por defecto

    if (!validarFormulario()) {
        showToast("Faltan completar campos obligatorios.");
        return;
    }

    // Mostrar modal de confirmación
    modal.style.display = "flex";
});


// --- Confirmación ---
confirmYes.addEventListener("click", () => {
    modal.style.display = "none";

    // Deshabilitar botón y poner loading
    btnEnviar.disabled = true;
    btnEnviar.textContent = "Enviando...";

    form.submit();  // ahora sí envía
});

confirmNo.addEventListener("click", () => {
    modal.style.display = "none";
});

// --- LIMPIAR ARCHIVO ---
btnLimpiar.addEventListener("click", () => {
    archivo.value = "";       // limpia el archivo
    archivo.classList.remove("error"); // borra error si lo había
    showToast("Archivo limpiado.");
});
