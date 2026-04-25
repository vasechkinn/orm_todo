function escapeHtml(value) {
    let str = '';
    if (value === null || value === undefined) {
        str = '';
    } else {
        str = String(value)
    }

    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/`/g, '&#x60;');
};
document.addEventListener('DOMContentLoaded', () => {

    let todosContainer = document.getElementById('todos_container');
    let btnFilter = document.getElementById('filter');
    let btnShowAll = document.getElementById('show_all');
    let btnClear = document.getElementById('clear');

    async function downloadTodos(params = {}) {
        todosContainer.innerHTML = '<p>download</p>';


        try {
            const url = new URL('/todo', window.location.origin);

            for (let [key, value] of Object.entries(params)) { // если парам пуст, то ничего не передаем 
                url.searchParams.append(key, value);
            }

            let response = await fetch(url);

            if (!response.ok) {
                todosContainer.innerHTML = `<p>error: ${response.status}</p>`;
                return;
            }

            let todos = await response.json();

            displayTodos(todos);
        } catch (error) {
            todosContainer.innerHTML = `<p>error: ${error.message}</p>`;
        }
    }

    function displayTodos(todos) {
        if (todos.length === 0) {
            todosContainer.innerHTML = '<p>no(</p>';
            return;
        }
        let ulContainerTodos = document.createElement('ul');

        todos.forEach(todo => {
            let li = document.createElement('li');

            li.innerHTML = `
            <p>title: ${escapeHtml(todo.title)}</p>
            <p>description: ${escapeHtml(todo.description)}</p>
            <p>is_completed: ${escapeHtml(todo.is_completed)}</p>
            `;

            ulContainerTodos.appendChild(li);
        });

        todosContainer.textContent = '';
        todosContainer.appendChild(ulContainerTodos);

    }
    if (btnShowAll) {
        btnShowAll.addEventListener('click', async () => {
            let filtersShow = document.getElementById('filters_show');
            filtersShow.textContent = '';
            await downloadTodos()
        });
    }

    if (btnClear) {
        btnClear.addEventListener('click', () => {
            let todosContainer = document.getElementById('todos_container');
            let filtersShow = document.getElementById('filters_show');
            filtersShow.textContent = '';
            todosContainer.textContent = '';
        })
    }

    if (btnFilter) {
        btnFilter.addEventListener('click', async () => {
            let todosContainer = document.getElementById('todos_container');
            todosContainer.textContent = '';
            let filtersShow = document.getElementById('filters_show');
            filtersShow.innerHTML = `
            <label>Skip:
                <input type="number" min="0" id="skip_todos">
            </label>
            <label>Limit:
                <input type="number" min="1" id="limit_todos">
            </label>
            <label>Is completed?
                <select id="is_completed_select">
                    <option value="">All</option>
                    <option value="true">Yes</option>
                    <option value="false">No</option>
                </select>
            </label>
            <button id='apply_btn'>apply</button>`;

            const applyBtn = document.getElementById('apply_btn');
            if (applyBtn) {
                applyBtn.addEventListener('click', () => {

                    const skip = document.getElementById('skip_todos').value;
                    const limit = document.getElementById('limit_todos').value;
                    const isCompleted = document.getElementById('is_completed_select').value;
        
                    const params = {
                        skip: parseInt(skip, 10) || 0,
                        limit: parseInt(limit, 10) || 10
                    };
        
                    if (isCompleted !== "") {
                        params.is_completed = isCompleted === 'true';
                    };
        
                    downloadTodos(params);
                })
            }
        });
    }
});