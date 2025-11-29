const modal = document.getElementById('filterModal');
const openBtn = document.getElementById('openFilterBtn');
const applyBtn = document.getElementById('applyBtn');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const priceFrom = document.getElementById('priceFrom');
const priceTo = document.getElementById('priceTo');

openBtn.addEventListener('click', function() {
    if (modal.style.display === 'block') {
        modal.style.display = 'none';
    } else {
        modal.style.display = 'block';
    }
});

window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

function getSearchUrl() {
    const currentPath = window.location.pathname;
    if (currentPath.includes('/balenciaga/')) {
        return '/balenciaga/search/';
    }
    return '/search/';
}

// Применение фильтров
applyBtn.addEventListener('click', function() {
    const query = searchInput.value.trim();
    const priceFromValue = priceFrom.value;
    const priceToValue = priceTo.value;
    
    // ИСПРАВЛЕНО: используем динамический путь
    let url = getSearchUrl();
    const params = [];
    
    if (query) {
        params.push(`q=${encodeURIComponent(query)}`);
    }
    if (priceFromValue) {
        params.push(`price_from=${priceFromValue}`);
    }
    if (priceToValue) {
        params.push(`price_to=${priceToValue}`);
    }
    
    if (params.length > 0) {
        url += '?' + params.join('&');
    }
    
    window.location.href = url;
});

// Функция поиска
function performSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        alert('Введите запрос для поиска');
        return;
    }
    
    // Сохраняем фильтры
    const priceFromValue = priceFrom ? priceFrom.value : '';
    const priceToValue = priceTo ? priceTo.value : '';
    
    // ИСПРАВЛЕНО: используем динамический путь
    let url = `${getSearchUrl()}?q=${encodeURIComponent(query)}`;
    
    if (priceFromValue) {
        url += `&price_from=${priceFromValue}`;
    }
    if (priceToValue) {
        url += `&price_to=${priceToValue}`;
    }
    
    window.location.href = url;
}

// Поиск по кнопке
if (searchBtn) {
    searchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        performSearch();
    });
}

// Поиск по Enter в поле ввода
if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch();
        }
    });
}

// Enter в полях фильтров
if (priceFrom) {
    priceFrom.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            applyBtn.click();
        }
    });
}

if (priceTo) {
    priceTo.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            applyBtn.click();
        }
    });
}