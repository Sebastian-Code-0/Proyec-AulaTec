document.addEventListener('DOMContentLoaded', function() {
    console.log("modal_grado.js cargado");

    const modal = document.getElementById('deleteModal');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.btn-cancel');
    const confirmDelete = document.getElementById('confirmDelete');
    const gradoName = document.getElementById('gradoName');
    
    let currentDeleteUrl = null;
    let currentDeleteButton = null;

    // Abrir modal 
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const name = this.getAttribute('data-grado-name');
            currentDeleteUrl = this.getAttribute('data-delete-url');
            currentDeleteButton = this;

            gradoName.textContent = `"${name}"`;
            modal.style.display = 'flex';
        });
    });

    // Confirmar eliminación 
    confirmDelete.addEventListener('click', function(e) {
        e.preventDefault();

        if (!currentDeleteUrl) return;

        confirmDelete.textContent = 'Eliminando...';
        confirmDelete.disabled = true;

        fetch(currentDeleteUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `csrfmiddlewaretoken=${getCookie('csrftoken')}`
        })
        .then(response => {
            if (response.ok) {
                if (currentDeleteButton) {
                    const row = currentDeleteButton.closest('tr');
                    row.style.transition = 'all 0.3s ease';
                    row.style.opacity = '0';
                    row.style.transform = 'translateX(-100%)';
                    setTimeout(() => row.remove(), 300);
                }
                closeModalFunc();
                showMessage('Grado eliminado correctamente', 'success');
            } else {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Error al eliminar el grado', 'error');
            confirmDelete.textContent = 'Sí, Eliminar';
            confirmDelete.disabled = false;
        });
    });

    // Función CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Mensajes flotantes 
    function showMessage(message, type) {
        const alertBox = document.createElement("div");
        alertBox.innerText = message;

        alertBox.style.position = "fixed";
        alertBox.style.top = "20px";
        alertBox.style.right = "20px";
        alertBox.style.padding = "12px 20px";
        alertBox.style.borderRadius = "8px";
        alertBox.style.color = "#fff";
        alertBox.style.zIndex = "9999";
        alertBox.style.fontWeight = "bold";
        alertBox.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
        alertBox.style.transition = "opacity 0.5s ease";

        if (type === "success") {
            alertBox.style.backgroundColor = "#28a745"; // verde
        } else {
            alertBox.style.backgroundColor = "#dc3545"; // rojo
        }

        document.body.appendChild(alertBox);

        setTimeout(() => {
            alertBox.style.opacity = "0";
            setTimeout(() => alertBox.remove(), 500);
        }, 3000);
    }

    // Cerrar modal 
    function closeModalFunc() {
        modal.style.display = 'none';
        confirmDelete.textContent = 'Sí, Eliminar';
        confirmDelete.disabled = false;
        currentDeleteUrl = null;
        currentDeleteButton = null;
    }

    closeModal.addEventListener('click', closeModalFunc);
    cancelBtn.addEventListener('click', closeModalFunc);
    modal.addEventListener('click', e => { if (e.target === modal) closeModalFunc(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModalFunc(); });
});
