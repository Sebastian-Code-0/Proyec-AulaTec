document.addEventListener('DOMContentLoaded', function() {
    console.log("modal_usuario.js cargado");

    const modal = document.getElementById('deleteModalUsuario');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.btn-cancel');
    const confirmDelete = document.getElementById('confirmDeleteUsuario');
    const usuarioName = document.getElementById('usuarioName');
    
    let currentUsuarioId = null;
    let currentUsuarioName = null;
    let currentDeleteUrl = null;

    // Función para obtener la cookie CSRF 
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Función global para cerrar el modal 
    function closeModalFunc() {
        modal.style.display = 'none';
        confirmDelete.textContent = 'Sí, Eliminar';
        confirmDelete.disabled = false;
    }

    // Función para mostrar mensajes flotantes
    function showMessage(message, type = "success") {
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

    // Abrir modal al dar click en "Eliminar" 
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            currentUsuarioId = this.getAttribute('data-usuario-id');
            currentUsuarioName = this.getAttribute('data-usuario-name');
            currentDeleteUrl = this.getAttribute('data-delete-url');

            usuarioName.textContent = `"${currentUsuarioName}"`;
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
                // Animar y eliminar la fila
                const rowToDelete = document.querySelector(`button[data-usuario-id="${currentUsuarioId}"]`).closest('tr');
                if (rowToDelete) {
                    rowToDelete.style.transition = 'all 0.3s ease';
                    rowToDelete.style.opacity = '0';
                    rowToDelete.style.transform = 'translateX(-100%)';
                    setTimeout(() => {
                        rowToDelete.remove();
                        const tbody = document.querySelector('tbody');
                        if (tbody && tbody.children.length === 0) {
                            window.location.reload();
                        }
                    }, 300);
                } else {
                    window.location.reload();
                }

                closeModalFunc();
                showMessage('Usuario eliminado correctamente', 'success');
            } else {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
        })
        .catch(error => {
            console.error('Error completo:', error);
            showMessage('Error al eliminar el usuario', 'error');
            confirmDelete.textContent = 'Sí, Eliminar';
            confirmDelete.disabled = false;
        });
    });

    // Eventos para cerrar modal con X o Cancelar 
    closeModal.addEventListener('click', closeModalFunc);
    cancelBtn.addEventListener('click', closeModalFunc);
    modal.addEventListener('click', e => { if (e.target === modal) closeModalFunc(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModalFunc(); });
});
