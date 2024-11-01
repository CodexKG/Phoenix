document.addEventListener('DOMContentLoaded', function () {
    // Сохранение состояния переключателя "канбан/таблица" в localStorage
    const switchToggle = document.getElementById('mz-switch-rounded');
    const kanbanBoard = document.getElementById('kanban-board-kanban');
    const tableBoard = document.getElementById('kanban-board-table');

    // Проверка состояния переключателя в localStorage
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

    // Обработчик для переключателя
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

    // Инициализация перетаскивания с помощью Sortable.js
    const listContainers = document.querySelectorAll('.sortable');

    listContainers.forEach(function (container) {
        new Sortable(container, {
            group: 'shared',
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
                        if (data.success) {
                            console.log('Позиции карточек обновлены');
                        } else {
                            console.error('Ошибка при обновлении карточек:', data.error);
                        }
                    })
                    .catch(error => console.error('Ошибка:', error));
            },
        });
    });

    // Управление модальными окнами для добавления и редактирования карточек
    const modal = document.getElementById('addCardModal');
    const closeModal = document.querySelector('.close');
    const addCardButtons = document.querySelectorAll('.add-card-btn');
    const form = document.getElementById('addCardForm');
    let currentListId = null;

    // Открытие модального окна
    addCardButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            currentListId = this.dataset.listId;
            modal.style.display = 'flex';
        });
    });

    // Закрытие модального окна
    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Закрытие модального окна при клике вне его
    window.addEventListener('click', function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Отправка формы для добавления карточки
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
                    const newCard = document.createElement('div');
                    newCard.classList.add('kanban-card');
                    newCard.innerHTML = `<h4>${data.card_title}</h4>`;
                    listContainer.appendChild(newCard);
                    modal.style.display = 'none';
                    form.reset();
                } else {
                    alert('Ошибка при добавлении карточки');
                }
            })
            .catch(error => console.error('Ошибка:', error));
    });

    // Управление модальными окнами для просмотра карточек
    const viewModal = document.getElementById('viewCardModal');
    const viewCloseIcon = document.getElementById('closeIcon');
    const viewCloseModal = document.getElementById('closeCardModal');
    const cards = document.querySelectorAll('.kanban-card');

    // Закрытие модального окна просмотра
    viewCloseModal.addEventListener('click', () => {
        viewModal.style.display = 'none';
    });

    viewCloseIcon.addEventListener('click', () => {
        viewModal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target == viewModal) {
            viewModal.style.display = 'none';
        }
    });

    // Добавляем обработчики для каждой карточки для просмотра информации
    cards.forEach(function (card) {
        card.addEventListener('click', function () {
            const cardTitle = this.querySelector('h4') ? this.querySelector('h4').innerText : "Нет названия";
            const cardDescription = this.querySelector('p') ? this.querySelector('p').innerText : "Нет описания";
            const cardDueDate = this.querySelector('p + p') ? this.querySelector('p + p').innerText : "Нет даты";

            const cardUser = this.dataset.user || "Нет пользователя";
            const cardCreatedAt = this.dataset.createdAt || "Не указана";
            const cardUpdatedAt = this.dataset.updatedAt || "Не указана";
            const cardAttachments = this.dataset.attachments || "";
            const cardMembers = this.dataset.members || "";

            document.getElementById('cardTitle').innerText = cardTitle;
            document.getElementById('cardDescription').innerText = cardDescription;
            document.getElementById('cardDueDate').innerText = cardDueDate;
            document.getElementById('cardUser').innerText = cardUser;
            document.getElementById('cardCreatedAt').innerText = cardCreatedAt;
            document.getElementById('cardUpdatedAt').innerText = cardUpdatedAt;

            const attachmentsList = document.getElementById('cardAttachments');
            attachmentsList.innerHTML = '';
            if (cardAttachments) {
                cardAttachments.split(',').forEach(attachment => {
                    const li = document.createElement('li');
                    li.textContent = attachment;
                    attachmentsList.appendChild(li);
                });
            }

            const membersList = document.getElementById('cardMembers');
            membersList.innerHTML = '';
            if (cardMembers) {
                cardMembers.split(',').forEach(member => {
                    const li = document.createElement('li');
                    li.textContent = member;
                    membersList.appendChild(li);
                });
            }

            viewModal.style.display = 'flex';
        });
    });

    // Удаление карточки
    const deleteButtons = document.querySelectorAll('.delete-card-btn');

    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            const kanbanCard = this.closest('.kanban-card');

            if (!kanbanCard) {
                console.error('kanban-card not found');
                return;
            }

            const cardId = kanbanCard.getAttribute('data-card-id');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            if (!cardId) {
                console.error('Card ID not found');
                return;
            }

            if (confirm('Вы уверены, что хотите удалить эту карточку?')) {
                fetch(`/admin/kanban/card/${cardId}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
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