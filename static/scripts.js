function escapeHtml(value) {
    let str = '';
    if (value === null || value === undefined) {
        str = '';
    }else {
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
            await downloadTodos()
        });
    }

    if (btnFilter) {
        btnFilter.addEventListener('click', async () => {
            await downloadTodos({
                limit: 10,
                skip: 0,
                is_completed: false
            }
            );
        });
    }
});