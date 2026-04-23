document.addEventListener('DOMContentLoaded', () => {
    let btnShowAll = document.getElementById('show_all');
    if (btnShowAll){
        
        btnShowAll.addEventListener('click', () => {
            window.location.href = '/'
        });
    }
    let btnFilter = document.getElementById('filter');
    if (btnFilter){

        btnFilter.addEventListener('click', () => {
            const params = new URLSearchParams();
            params.set('limit', 100);
            params.set('skip', 0);
            params.set('is_completed', 'false');
            window.location.href = '/?' + params.toString();
        });
    }
    }
);