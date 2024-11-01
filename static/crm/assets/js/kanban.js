document.addEventListener('DOMContentLoaded', function () {
    // Получаем переключатель и контейнеры представлений (канбан и таблицу)
    const switchToggle = document.getElementById('mz-switch-rounded');
    const kanbanBoard = document.getElementById('kanban-board-kanban');
    const tableBoard = document.getElementById('kanban-board-table');

    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';
    if (!csrfToken) {
        console.error('CSRF-токен не найден');
    }

    // Проверяем сохраненное состояние переключателя из localStorage и применяем нужное представление
    const savedState = localStorage.getItem('boardView');
    if (savedState === 'table') {
        switchToggle.checked = true;
        kanbanBoard.classList.add('hidden');
        kanbanBoard.classList.remove('visible');
        tableBoard.classList.add('visible');
        tableBoard.classList.remove('hidden');
    } else {
        switchToggle.checked = false;
        kanbanBoard.classList.add('visible');
        kanbanBoard.classList.remove('hidden');
        tableBoard.classList.add('hidden');
        tableBoard.classList.remove('visible');
    }

    // Обработчик переключателя между канбаном и таблицей
    switchToggle.addEventListener('change', function () {
        if (switchToggle.checked) {
            kanbanBoard.classList.add('hidden');
            kanbanBoard.classList.remove('visible');
            tableBoard.classList.add('visible');
            tableBoard.classList.remove('hidden');
            localStorage.setItem('boardView', 'table');
        } else {
            kanbanBoard.classList.add('visible');
            kanbanBoard.classList.remove('hidden');
            tableBoard.classList.add('hidden');
            tableBoard.classList.remove('visible');
            localStorage.setItem('boardView', 'kanban');
        }
    });

    // Инициализация Sortable.js для перемещения карточек в канбан-доске
    const listContainers = document.querySelectorAll('.sortable');
    listContainers.forEach(function (container) {
        new Sortable(container, {
            group: 'kanban',
            animation: 150,
            ghostClass: 'sortable-ghost',
            onEnd: function (evt) {
                const cardIds = Array.from(evt.to.children)
                    .map(card => card.dataset.cardId)
                    .filter(id => id !== null && id !== undefined);

                const listId = evt.to.getAttribute('data-list-id');
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch('/admin/kanban/update_card_positions/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        listId: listId,
                        cardIds: cardIds
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        console.error('Ошибка при обновлении позиций карточек:', data.error);
                    }
                })
                .catch(error => console.error('Ошибка:', error));
            }
        });
    });

    // Управление модальным окном для добавления карточек
    const modal = document.getElementById('addCardModal');
    const closeModal = document.querySelector('.close');
    const addCardButtons = document.querySelectorAll('.add-card-btn');
    const form = document.getElementById('addCardForm');
    let currentListId = null;

    addCardButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            currentListId = this.dataset.listId;
            modal.style.display = 'flex';
        });
    });

    closeModal.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (event) => {
        if (event.target === modal) modal.style.display = 'none';
    });

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/admin/kanban/list/${currentListId}/add_card/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const listContainer = document.querySelector(`#list-${currentListId} .kanban-cards`);
                    if (listContainer && data.card_id && data.card_title) {
                        const newCard = document.createElement('div');
                        newCard.classList.add('kanban-card');
                        newCard.dataset.cardId = data.card_id;
                        newCard.innerHTML = `<h3>${data.card_title}</h3>`;
                        listContainer.appendChild(newCard);
                    } else {
                        console.error('Не удалось создать карточку. Проверьте данные.');
                    }
                    modal.style.display = 'none';
                    form.reset();
                } else {
                    alert('Ошибка при добавлении карточки');
                }
            })
            .catch(error => console.error('Ошибка:', error));
        });
    } else {
        console.error('Элемент формы не найден');
    }

    // Управление модальным окном для добавления списка
    const addListModal = document.getElementById('addListModal');
    const openAddListModalButton = document.getElementById('openAddListModal');
    const closeAddListModalButton = addListModal.querySelector('.close');
    const addListForm = document.getElementById('addListForm');

    openAddListModalButton.addEventListener('click', function () {
        addListModal.style.display = 'flex';
    });

    closeAddListModalButton.addEventListener('click', function () {
        addListModal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === addListModal) {
            addListModal.style.display = 'none';
        }
    });

    // Отправка формы для добавления списка
    addListForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(addListForm);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        fetch(addListUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {  // Убедитесь, что проверка success соответствует вашему ответу сервера
                addListModal.style.display = 'none';
                addListForm.reset();
                location.reload(); // Перезагрузка страницы после успешного добавления
            } else {
                console.error('Ошибка данных сервера:', data);
                alert('Ошибка при добавлении списка');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    });

    // Управление модальным окном для просмотра карточки
    const viewModal = document.getElementById('viewCardModal');
    const viewCloseIcon = document.getElementById('closeIcon');
    const viewCloseModal = document.getElementById('closeCardModal');

    function showModalWithCardData(card) {
        document.getElementById('cardTitle').innerText = card.querySelector('h4')?.innerText || "Нет названия";
        document.getElementById('cardDescription').innerText = card.querySelector('p')?.innerText || "Нет описания";
        viewModal.style.display = 'flex';
    }

    viewCloseIcon.addEventListener('click', () => viewModal.style.display = 'none');
    viewCloseModal.addEventListener('click', () => viewModal.style.display = 'none');
    window.addEventListener('click', (event) => {
        if (event.target === viewModal) viewModal.style.display = 'none';
    });

    function addCardClickListeners() {
        document.querySelectorAll('.kanban-card').forEach(card => {
            card.addEventListener('click', () => showModalWithCardData(card));
        });

        document.querySelectorAll('.table-card').forEach(card => {
            card.addEventListener('click', () => showModalWithCardData(card));
        });
    }

    addCardClickListeners();

    document.querySelectorAll('.delete-card-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            const kanbanCard = this.closest('.kanban-card') || this.closest('.table-card');
            const cardId = kanbanCard?.dataset.cardId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            if (cardId && confirm('Вы уверены, что хотите удалить эту карточку?')) {
                fetch(`/admin/kanban/card/${cardId}/delete/`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrfToken }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        kanbanCard.remove();
                        alert('Карточка удалена');
                    } else {
                        alert('Ошибка удаления карточки: ' + data.error);
                    }
                })
                .catch(error => console.error('Ошибка:', error));
            }
        });
    });
});