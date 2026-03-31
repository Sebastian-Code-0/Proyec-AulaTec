document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('deleteModalMatricula');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.btn-cancel');
    const confirmDelete = document.getElementById('confirmDeleteMatricula');
    const matriculaName = document.getElementById('matriculaName');

    let currentDeleteUrl = null;
    let currentDeleteButton = null;

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

    function showMessage(message, type = 'success') {
        const alertBox = document.createElement('div');
        alertBox.innerText = message;
        alertBox.style.cssText = 'position:fixed;top:20px;right:20px;padding:12px 18px;border-radius:8px;color:#fff;z-index:9999;font-weight:700;box-shadow:0 2px 6px rgba(0,0,0,0.2);transition:opacity 0.4s ease;';
        alertBox.style.backgroundColor = type === 'success' ? '#10B981' : '#EF4444';
        document.body.appendChild(alertBox);
        setTimeout(() => {
            alertBox.style.opacity = '0';
            setTimeout(() => alertBox.remove(), 400);
        }, 2600);
    }

    function closeModalFunc() {
        if (!modal) return;
        modal.style.display = 'none';
        confirmDelete.textContent = 'Sí, Eliminar';
        confirmDelete.disabled = false;
        currentDeleteUrl = null;
        currentDeleteButton = null;
        if (matriculaName) matriculaName.textContent = '';
    }

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const name = this.getAttribute('data-matricula-name') || '—';
            currentDeleteUrl = this.getAttribute('data-delete-url');
            currentDeleteButton = this;
            if (matriculaName) matriculaName.textContent = '"' + name + '"';
            modal.style.display = 'flex';
        });
    });

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
            body: 'csrfmiddlewaretoken=' + getCookie('csrftoken')
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
                            if (tbody && tbody.children.length === 0) window.location.reload();
                        }, 300);
                    }
                }
                closeModalFunc();
                showMessage('Matrícula eliminada correctamente', 'success');
            } else {
                throw new Error('Error ' + response.status);
            }
        })
        .catch(error => {
            showMessage('Error al eliminar la matrícula', 'error');
            confirmDelete.textContent = 'Sí, Eliminar';
            confirmDelete.disabled = false;
        });
    });

    if (closeModal) closeModal.addEventListener('click', closeModalFunc);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModalFunc);
    if (modal) modal.addEventListener('click', e => { if (e.target === modal) closeModalFunc(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModalFunc(); });
});
