(function () {
    var key = 'balenciaga_views';
    var count = parseInt(sessionStorage.getItem(key) || '0', 10) + 1;
    sessionStorage.setItem(key, count);

    function init() {
        var main = document.querySelector('main');
        if (!main) return;

        var bar = document.createElement('div');
        bar.id = 'view-counter';
        bar.style.cssText = [
            'text-align:center',
            'padding:10px 0 6px',
            'font-size:12px',
            'font-family:sans-serif',
            'letter-spacing:2px',
            'color:#aaa',
            'position:relative',
            'z-index:0'
        ].join(';');
        bar.textContent = 'ПРОСМОТРОВ ЗА СЕССИЮ: ' + count;
        main.appendChild(bar);

        var h1 = main.querySelector('h1');
        if (h1) {
            main.insertBefore(bar, h1.nextSibling);
        } else {
            main.insertBefore(bar, main.firstChild);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
