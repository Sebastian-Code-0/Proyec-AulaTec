document.addEventListener('DOMContentLoaded', function() {
    console.log("modal_docente.js cargado ");

    const modal = document.getElementById('deleteModal');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.btn-cancel');
    const confirmDelete = document.getElementById('confirmDelete');
    const docenteName = document.getElementById('docenteName');

    let currentDeleteUrl = null;
    let currentDeleteButton = null;

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

    // Mostrar mensajes
    function showMessage(message, type = "success") {
        const alertBox = document.createElement("div");
        alertBox.innerText = message;
        alertBox.style.position = "fixed";
        alertBox.style.top = "20px";
        alertBox.style.right = "20px";
        alertBox.style.padding = "12px 18px";
        alertBox.style.borderRadius = "8px";
        alertBox.style.color = "#fff";
        alertBox.style.zIndex = "9999";
        alertBox.style.fontWeight = "700";
        alertBox.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
        alertBox.style.transition = "opacity 0.4s ease";
        alertBox.style.backgroundColor = (type === "success") ? "#28a745" : "#dc3545";

        document.body.appendChild(alertBox);
        setTimeout(() => {
            alertBox.style.opacity = "0";
            setTimeout(() => alertBox.remove(), 400);
        }, 2600);
    }

    // Cerrar modal 
    function closeModalFunc() {
        if (!modal) return;
        modal.style.display = 'none';
        confirmDelete.textContent = 'Sí, Eliminar';
        confirmDelete.disabled = false;
        currentDeleteUrl = null;
        currentDeleteButton = null;
        docenteName.textContent = '';
    }

    // Abrir modal 
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const name = this.getAttribute('data-docente-name') || '—';
            currentDeleteUrl = this.getAttribute('data-delete-url');
            currentDeleteButton = this;

            docenteName.textContent = `"${name}"`;
            modal.style.display = 'flex';
        });
    });

    // Confirmar eliminación 
    confirmDelete.addEventListener('click', function(e) {
        e.preventDefault();

        if (!currentDeleteUrl) {
            showMessage('URL de eliminación inválida', 'error');
            return;
        }

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
                    if (row) {
                        row.style.transition = 'all 0.3s ease';
                        row.style.opacity = '0';
                        row.style.transform = 'translateX(-100%)';
                        setTimeout(() => {
                            row.remove();
                            const tbody = document.querySelector('tbody');
                            if (tbody && tbody.children.length === 0) {
                                window.location.reload();
                            }
                        }, 300);
                    }
                }
                closeModalFunc();
                showMessage('Docente eliminado correctamente', 'success');
            } else {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
        })
        .catch(error => {
            console.error('Error al eliminar docente:', error);
            showMessage('Error al eliminar el docente', 'error');
            confirmDelete.textContent = 'Sí, Eliminar';
            confirmDelete.disabled = false;
        });
    });

    // Eventos de cierre 
    if (closeModal) closeModal.addEventListener('click', closeModalFunc);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModalFunc);
    if (modal) modal.addEventListener('click', e => { if (e.target === modal) closeModalFunc(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModalFunc(); });
});
