document.addEventListener('DOMContentLoaded', function () {
    // Получаем переключатель и контейнеры представлений (канбан и таблицу)
    const switchToggle = document.getElementById('mz-switch-rounded');
    const kanbanBoard = document.getElementById('kanban-board-kanban');
    const tableBoard = document.getElementById('kanban-board-table');

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
            // Скрыть канбан и показать таблицу
            kanbanBoard.classList.add('hidden');
            kanbanBoard.classList.remove('visible');
            tableBoard.classList.add('visible');
            tableBoard.classList.remove('hidden');
            localStorage.setItem('boardView', 'table'); // Сохранить состояние в localStorage
        } else {
            // Показать канбан и скрыть таблицу
            kanbanBoard.classList.add('visible');
            kanbanBoard.classList.remove('hidden');
            tableBoard.classList.add('hidden');
            tableBoard.classList.remove('visible');
            localStorage.setItem('boardView', 'kanban'); // Сохранить состояние в localStorage
        }
    });

    // Инициализация Sortable.js для перемещения карточек в канбан-доске
    const listContainers = document.querySelectorAll('.sortable');
    listContainers.forEach(function (container) {
        new Sortable(container, {
            group: 'kanban', // Объединяем контейнеры в одну группу для перетаскивания
            animation: 150, // Анимация перемещения
            ghostClass: 'sortable-ghost', // Класс для выделения перетаскиваемого элемента
            onEnd: function (evt) {
                // Обновление положения карточек на сервере после перетаскивания
                const cardIds = Array.from(evt.to.children)
                    .map(card => card.dataset.cardId)
                    .filter(id => id !== null && id !== undefined);

                const listId = evt.to.getAttribute('data-list-id');
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                // Отправляем обновленные позиции карточек на сервер
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
    let currentListId = null; // ID списка, в который добавляется карточка

    // Открытие модального окна для добавления карточки
    addCardButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            currentListId = this.dataset.listId; // Запоминаем список, в который добавляется карточка
            modal.style.display = 'flex';
        });
    });

    // Закрытие модального окна для добавления карточки
    closeModal.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (event) => {
        if (event.target === modal) modal.style.display = 'none';
    });

    // Обработка формы добавления карточки
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
                // Создаем новый элемент карточки и добавляем его в текущий список
                const listContainer = document.querySelector(`#list-${currentListId} .kanban-cards`);
                const newCard = document.createElement('div');
                newCard.classList.add('kanban-card');
                newCard.dataset.cardId = data.card_id;
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

    // Управление модальным окном для просмотра карточки
    const viewModal = document.getElementById('viewCardModal');
    const viewCloseIcon = document.getElementById('closeIcon');
    const viewCloseModal = document.getElementById('closeCardModal');

    // Функция для отображения данных карточки в модальном окне
    function showModalWithCardData(card) {
        document.getElementById('cardTitle').innerText = card.querySelector('h4')?.innerText || "Нет названия";
        document.getElementById('cardDescription').innerText = card.querySelector('p')?.innerText || "Нет описания";
        viewModal.style.display = 'flex';
    }

    // Закрытие модального окна просмотра
    viewCloseIcon.addEventListener('click', () => viewModal.style.display = 'none');
    viewCloseModal.addEventListener('click', () => viewModal.style.display = 'none');
    window.addEventListener('click', (event) => {
        if (event.target === viewModal) viewModal.style.display = 'none';
    });

    // Добавляем обработчики для открытия модального окна просмотра карточек в канбане и таблице
    function addCardClickListeners() {
        // Добавляем обработчики для карточек в канбан-доске
        document.querySelectorAll('.kanban-card').forEach(card => {
            card.addEventListener('click', () => showModalWithCardData(card));
        });

        // Добавляем обработчики для карточек в табличном представлении
        document.querySelectorAll('.table-card').forEach(card => {
            card.addEventListener('click', () => showModalWithCardData(card));
        });
    }

    // Инициализируем обработчики для всех карточек при загрузке страницы
    addCardClickListeners();

    // Удаление карточки
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