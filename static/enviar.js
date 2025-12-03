const form = document.getElementById("envioForm");
const toast = document.getElementById("toast");
const confirmModal = document.getElementById("confirmModal");
const confirmYes = document.getElementById("confirmYes");
const confirmNo = document.getElementById("confirmNo");
const btnEnviar = document.getElementById("btnEnviar");
const btnLimpiar = document.getElementById("btnLimpiar");
const archivo = document.getElementById("archivo");
const fileLabel = document.querySelector(".archivo-personalizado");

const infoButton = document.querySelector(".btnInfo");
const infoModal = document.getElementById("infoModal");

if (window.SERVER_ERROR) {
    showToast(window.SERVER_ERROR, "error");
}

if (window.SERVER_SUCCESS) {
    showToast(window.SERVER_SUCCESS, "success");
}

function showToast(message, type = "error") {
    toast.textContent = message;
    toast.classList.remove("toast-error", "toast-success");
    if (type === "success") {
        toast.classList.add("toast-success");
    } else {
        toast.classList.add("toast-error");
    }
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 9000);
}

function validarFormulario() {
    let valido = true;

    document.querySelectorAll(".error").forEach(e => e.classList.remove("error"));

    const asunto = document.getElementById("asunto");
    const texto = document.getElementById("texto");
    const correo = document.getElementById("correo");
    const pass = document.getElementById("contraseniaSec");
    const archivoInput = document.getElementById("archivo");

    if (!asunto.value.trim()) {
        asunto.classList.add("error");
        valido = false;
    }
    if (!texto.value.trim()) {
        texto.classList.add("error");
        valido = false;
    }
    if (!correo.value.trim()) {
        correo.classList.add("error");
        valido = false;
    }
    if (!pass.value.trim()) {
        pass.classList.add("error");
        valido = false;
    }

    const fileName = archivoInput.value.toLowerCase();
    if (!fileName.endsWith(".xlsx") && !fileName.endsWith(".xls")) {
        archivoInput.classList.add("error");
        valido = false;
        showToast("El archivo debe ser Excel (.xlsx o .xls)", "error");
    }

    return valido;
}

form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!validarFormulario()) {
        showToast("Faltan completar campos obligatorios.", "error");
        return;
    }

    confirmModal.style.display = "flex";
});

confirmYes.addEventListener("click", () => {
    confirmModal.style.display = "none";
    btnEnviar.disabled = true;
    btnEnviar.textContent = "Enviando...";
    form.submit();
});

confirmNo.addEventListener("click", () => {
    confirmModal.style.display = "none";
});

btnLimpiar.addEventListener("click", () => {
    archivo.value = "";
    archivo.classList.remove("error");
    fileLabel.textContent = "Selecciona un archivo";
    showToast("Archivo limpiado.", "success");
});

if (infoButton && infoModal) {
    infoButton.addEventListener("click", (e) => {
        e.stopPropagation();
        infoModal.classList.toggle("show");
    });

    document.addEventListener("click", (e) => {
        if (!infoModal.classList.contains("show")) return;
        const isClickInside = infoModal.contains(e.target) || infoButton.contains(e.target);
        if (!isClickInside) {
            infoModal.classList.remove("show");
        }
    });

    archivo.addEventListener("change", () => {
        if (archivo.files.length > 0) {
            fileLabel.textContent = archivo.files[0].name;
        } else {
            fileLabel.textContent = "Selecciona un archivo";
        }
    });
}
