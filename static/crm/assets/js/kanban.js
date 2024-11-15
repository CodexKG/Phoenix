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
        // Обновление сообщений "Нет задач" после переключения
        document.querySelectorAll('.kanban-list').forEach(function (listElement) {
            toggleEmptyMessage(listElement);
        });
        document.querySelectorAll('.table-list').forEach(function (listElement) {
            toggleEmptyMessage(listElement);
        });
    });

    // Функция для обновления сообщения "Нет задач в этом списке"
    function updateEmptyMessage(listElement) {
        const noTasksMessage = listElement.querySelector('.no-tasks-message');
        const hasCards = listElement.querySelectorAll('.kanban-card, .table-card').length > 0;

        if (noTasksMessage) {
            noTasksMessage.style.display = hasCards ? 'none' : 'block';
        }
    }

    // Первоначальная инициализация Sortable.js для всех списков
    initializeSortable();



    function initializeSortable() {
        const kanbanContainers = document.querySelectorAll('.kanban-cards');
        const tableContainers = document.querySelectorAll('.table-cards');

        kanbanContainers.forEach(container => {
            new Sortable(container, {
                group: 'shared',
                animation: 150,
                ghostClass: 'sortable-ghost',
                onEnd: function (evt) {
                    const listId = evt.to.dataset.listId;
                    const cardIds = Array.from(evt.to.children)
                        .map(card => card.dataset.cardId)
                        .filter(id => id !== null && id !== undefined); // Только валидные ID

                    toggleEmptyMessage(evt.from.closest('.kanban-list'));
                    toggleEmptyMessage(evt.to.closest('.kanban-list'));
                    syncAndSave(listId, cardIds, 'table');
                }
            });
        });

        tableContainers.forEach(container => {
            new Sortable(container, {
                group: 'shared',
                animation: 150,
                ghostClass: 'sortable-ghost',
                onEnd: function (evt) {
                    const listId = evt.to.dataset.listId;
                    const cardIds = Array.from(evt.to.children)
                        .map(card => card.dataset.cardId)
                        .filter(id => id !== null && id !== undefined); // Только валидные ID

                    toggleEmptyMessage(evt.from.closest('.table-list'));
                    toggleEmptyMessage(evt.to.closest('.table-list'));
                    syncAndSave(listId, cardIds, 'kanban');
                }
            });
        });
    }

    function toggleEmptyMessage(container) {
        if (container) {
            const noTasksMessage = container.querySelector('.no-tasks-message');
            const hasTasks = container.querySelectorAll('.kanban-card, .table-card').length > 0;
            if (noTasksMessage) {
                noTasksMessage.style.display = hasTasks ? 'none' : 'block';
            }
        }
    }

    function updateTableOrder(listId, cardIds) {
        const tableContainer = document.querySelector(`.table-cards[data-list-id="${listId}"]`);
        if (tableContainer) {
            tableContainer.innerHTML = '';  // Очищаем таблицу перед обновлением

            cardIds.forEach(cardId => {
                const existingTableCard = document.querySelector(`.table-card[data-card-id="${cardId}"]`);
                if (existingTableCard) {
                    existingTableCard.remove();
                }

                const kanbanCard = document.querySelector(`.kanban-card[data-card-id="${cardId}"]`);
                if (kanbanCard) {
                    const tableCard = document.createElement('div');
                    tableCard.classList.add('table-card');
                    tableCard.dataset.cardId = cardId;
                    tableCard.innerHTML = `
                        <img width="20" src="https://icons.veryicon.com/png/o/miscellaneous/linear-icon-45/hamburger-menu-4.png" alt="">
                        <b>✅ ${kanbanCard.querySelector('h4').innerText}</b>
                        <p>${kanbanCard.querySelector('p').innerText}</p>
                    `;
                    tableContainer.appendChild(tableCard);
                }
            });

            toggleEmptyMessage(tableContainer.closest('.table-list'));
        }
    }

    function updateKanbanOrder(listId, cardIds) {
        const kanbanContainer = document.querySelector(`.kanban-cards[data-list-id="${listId}"]`);
        if (kanbanContainer) {
            kanbanContainer.innerHTML = '';  // Очищаем канбан перед обновлением

            cardIds.forEach(cardId => {
                const existingKanbanCard = document.querySelector(`.kanban-card[data-card-id="${cardId}"]`);
                if (existingKanbanCard) {
                    existingKanbanCard.remove();
                }

                const tableCard = document.querySelector(`.table-card[data-card-id="${cardId}"]`);
                if (tableCard) {
                    const kanbanCard = document.createElement('div');
                    kanbanCard.classList.add('kanban-card');
                    kanbanCard.dataset.cardId = cardId;
                    kanbanCard.innerHTML = `
                        <h4>${tableCard.querySelector('b').innerText}</h4>
                        <p>${tableCard.querySelector('p').innerText}</p>
                    `;
                    kanbanContainer.appendChild(kanbanCard);
                }
            });

            toggleEmptyMessage(kanbanContainer.closest('.kanban-list'));
        }
    }


    function syncAndSave(listId, cardIds, target) {
        if (target === 'table') {
            updateTableOrder(listId, cardIds);
        } else if (target === 'kanban') {
            updateKanbanOrder(listId, cardIds);
        }

        fetch('/admin/kanban/update_card_positions/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ listId: listId, cardIds: cardIds })
        })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.error('Ошибка при сохранении порядка на сервере:', data.error);
                } else {
                    // Обновляем сообщения о пустоте для каждого списка на основе данных с сервера
                    if (data.taskCounts) {
                        for (let [listId, count] of Object.entries(data.taskCounts)) {
                            const listContainer = document.querySelector(`[data-list-id="${listId}"]`);
                            if (listContainer) {
                                const noTasksMessage = listContainer.querySelector('.no-tasks-message');
                                if (noTasksMessage) {
                                    noTasksMessage.style.display = count > 0 ? 'none' : 'block';
                                }
                            }
                        }
                    }
                }
            })
            .catch(error => console.error('Ошибка при сохранении порядка:', error));
    }

    // Обновляем сообщение для каждого списка при загрузке страницы
    document.querySelectorAll('.kanban-list').forEach(function (listElement) {
        updateEmptyMessage(listElement);
    });
    document.querySelectorAll('.table-list').forEach(function (listElement) {
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
                        throw new Error(`HTTP error! status: ${response}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data)
                    if (data.success) {
                        const listContainer = document.querySelector(`#list-${currentListId} .kanban-cards`);
                        const listContainer2 = document.querySelector(`#table-list-${currentListId} .table-cards`);
                        if (listContainer || listContainer2 && data.card_id && data.card_title) {
                            const newCard = document.createElement('div');
                            newCard.classList.add('kanban-card');
                            newCard.dataset.cardId = data.card_id;
                            newCard.innerHTML = `<h4>${data.card_title}</h4><p>${data.card_description}</p>`;
                            listContainer.appendChild(newCard);
                            updateEmptyMessage(listContainer.closest('.kanban-list'));

                            const newCard2 = document.createElement('div');
                            newCard2.classList.add('table-card');
                            newCard2.dataset.cardId = data.card_id;
                            newCard2.innerHTML = `
                             <img width="20" src="https://icons.veryicon.com/png/o/miscellaneous/linear-icon-45/hamburger-menu-4.png" alt=""><b>✅ ${data.card_title}</b><p>${data.card_description}</p>`;
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
                    console.log(error)
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
        // Лог для проверки переданных данных карточки
        console.log('Card data:', card);

        // Получение данных карточки
        document.getElementById('cardTitle').innerText = card.dataset.title || "Нет названия";
        document.getElementById('cardDescription').innerText = card.dataset.description || "Нет описания";
        document.getElementById('cardDueDate').innerText = card.dataset.dueDate || "Нет данных";
        document.getElementById('cardUser').innerText = card.dataset.user || "Не указано";
        document.getElementById('cardCreatedAt').innerText = card.dataset.createdAt || "Нет данных";
        document.getElementById('cardUpdatedAt').innerText = card.dataset.updatedAt || "Нет данных";

        // Найдём элемент вложений по уникальному ID карточки
        const cardId = card.dataset.cardId;

        // Выполняем fetch для получения вложений с сервера
        fetch(`/admin/kanban/card/${cardId}/attachments/`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => response.json())
            .then(data => {
                // Очищаем модальное окно вложений перед добавлением новых данных
                const attachmentsModalList = document.getElementById('cardAttachmentsModal');

                if (attachmentsModalList) {
                    attachmentsModalList.innerHTML = '';
                } else {
                    console.error('Элемент cardAttachmentsModal не найден');
                    return;
                }

                if (data.success && data.attachments.length > 0) {
                    // Добавляем вложения в модальное окно
                    data.attachments.forEach(attachment => {
                        const li = document.createElement('li');
                        const a = document.createElement('a');
                        a.href = attachment.file_url;
                        a.target = '_blank';
                        a.textContent = attachment.file_name;
                        li.appendChild(a);
                        attachmentsModalList.appendChild(li);
                    });
                } else {
                    // Если вложений нет, отображаем сообщение "Нет вложений"
                    const li = document.createElement('li');
                    li.textContent = 'Нет вложений';
                    attachmentsModalList.appendChild(li);
                }

                // Открываем модальное окно
                const viewModal = document.getElementById('viewCardModal');
                if (viewModal) {
                    viewModal.style.display = 'flex';
                }
            })
            .catch(error => {
                console.error('Ошибка при получении вложений:', error);

                // Открываем модальное окно и показываем сообщение об ошибке
                const attachmentsModalList = document.getElementById('cardAttachmentsModal');
                if (attachmentsModalList) {
                    const li = document.createElement('li');
                    li.textContent = 'Ошибка при загрузке вложений';
                    attachmentsModalList.appendChild(li);
                }

                const viewModal = document.getElementById('viewCardModal');
                if (viewModal) {
                    viewModal.style.display = 'flex';
                }
            });
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