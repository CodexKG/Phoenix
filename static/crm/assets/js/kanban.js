document.addEventListener('DOMContentLoaded', function () {
    // Получаем переключатель и контейнеры представлений (канбан и таблицу)
    const switchToggle = document.getElementById('mz-switch-rounded');
    const kanbanBoard = document.getElementById('kanban-board-kanban');
    const tableBoard = document.getElementById('kanban-board-table');

    // Получаем CSRF-токен для отправки запросов на сервер
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
        initializeSortable(); // Переинициализация Sortable.js при переключении режима
    });

    // Функция для обновления сообщения "Нет задач в этом списке"
    function updateEmptyMessage(listElement) {
        const noTasksMessage = listElement.querySelector('.no-tasks-message');
        const hasCards = listElement.querySelectorAll('.kanban-card, .table-card').length > 0;

        if (noTasksMessage) {
            noTasksMessage.style.display = hasCards ? 'none' : 'block';
        }
    }

    // Функция для инициализации Sortable.js для перемещения карточек в канбан-доске и таблице
    function initializeSortable() {
        const listContainers = document.querySelectorAll('.sortable');
        listContainers.forEach(function (container) {
            new Sortable(container, {
                group: 'kanban',
                animation: 150,
                ghostClass: 'sortable-ghost',
                onEnd: function (evt) {
                    // Обновляем пустые сообщения в обоих списках: отправителе и получателе
                    updateEmptyMessage(evt.from.closest('.kanban-list, tr'));
                    updateEmptyMessage(evt.to.closest('.kanban-list, tr'));

                    // Обновление позиций карточек на сервере
                    const cardIds = Array.from(evt.to.children)
                        .map(card => card.dataset.cardId)
                        .filter(id => id !== null && id !== undefined);

                    const listId = evt.to.getAttribute('data-list-id');
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
    }

    // Первоначальная инициализация Sortable.js для всех списков
    initializeSortable();

    // Обновляем сообщение для каждого списка при загрузке страницы
    document.querySelectorAll('.kanban-list').forEach(function (listElement) {
        updateEmptyMessage(listElement);
    });

    // Управление модальным окном для добавления карточек
    const modal = document.getElementById('addCardModal');
    const closeModal = document.querySelector('.close');
    const addCardButtons = document.querySelectorAll('.add-card-btn');
    const form = document.getElementById('addCardForm');
    let currentListId = null;

    // Открытие модального окна для добавления карточки
    addCardButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            currentListId = this.dataset.listId;
            modal.style.display = 'flex';
        });
    });

    // Закрытие модального окна
    closeModal.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (event) => {
        if (event.target === modal) modal.style.display = 'none';
    });

    // Обработка формы добавления карточки
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/admin/kanban/list/${currentListId}/add_card/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken // Передаем CSRF-токен для безопасности
                },
                body: formData // Отправляем данные формы, включая файлы
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        const listContainer = document.querySelector(`#list-${currentListId} .kanban-cards`);
                        const listContainer2 = document.querySelector(`#table-list-${currentListId} .table-cards`);
                        if (listContainer || listContainer2 && data.card_id && data.card_title) {
                            const newCard = document.createElement('div');
                            newCard.classList.add('kanban-card');
                            newCard.dataset.cardId = data.card_id;
                            newCard.innerHTML = `<h3>${data.card_title}</h3>`;
                            listContainer.appendChild(newCard);
                            updateEmptyMessage(listContainer.closest('.kanban-list'));

                            const newCard2 = document.createElement('div');
                            newCard2.classList.add('table-card');
                            newCard2.dataset.cardId = data.card_id;
                            newCard2.innerHTML = `
                             <img width="20" src="https://icons.veryicon.com/png/o/miscellaneous/linear-icon-45/hamburger-menu-4.png" alt=""><b>✅ ${data.card_title}</b> `;
                            listContainer2.appendChild(newCard2);
                            updateEmptyMessage(listContainer2.closest('.table-list'));
                        } else {
                            console.error('Не удалось создать карточку. Проверьте данные.');
                        }
                        modal.style.display = 'none';
                        form.reset();
                    } else {
                        alert('Ошибка при добавлении карточки');
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert('Произошла ошибка при добавлении карточки. Пожалуйста, попробуйте еще раз.');
                });
        });
    }

    // Функция для открытия модального окна для добавления вложений
    function openAttachmentModal() {
        const attachmentModal = document.getElementById('addAttachmentModal');
        if (attachmentModal) {
            attachmentModal.style.display = 'flex';
        }
    }

    // Управление модальным окном для добавления вложений
    const attachmentForm = document.getElementById('addAttachmentForm');
    if (attachmentForm) {
        attachmentForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(attachmentForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/admin/kanban/card/${currentCardId}/add_attachment/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(`Файл ${data.file_name} успешно добавлен`);
                        attachmentForm.reset();
                    } else {
                        alert('Ошибка при добавлении вложения');
                    }
                })
                .catch(error => console.error('Ошибка:', error));
        });
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
                if (data.success) {  // Проверка успешности ответа
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

    // Добавление событий для нажатия на карточки
    function addCardClickListeners() {
        document.querySelectorAll('.kanban-card').forEach(card => {
            card.addEventListener('click', () => showModalWithCardData(card));
        });

        document.querySelectorAll('.table-card').forEach(card => {
            card.addEventListener('click', () => showModalWithCardData(card));
        });
    }

    addCardClickListeners();

    // Добавление событий для кнопок удаления карточек
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
                            updateEmptyMessage(kanbanCard.closest('.kanban-list'));
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