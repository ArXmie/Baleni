(function () {
    var btn = document.createElement('button');
    btn.id = 'scrollTopBtn';
    btn.textContent = '↑';
    btn.style.cssText = [
        'position:fixed',
        'bottom:120px',
        'right:24px',
        'width:44px',
        'height:44px',
        'background:rgb(255 255 255)',
        'color:rgb(0 0 0)',
        'border:1.2px solid rgb(0, 0, 0)',
        'font-size:20px',
        'cursor:pointer',
        'opacity:0',
        'transition:opacity 0.3s ease',
        'z-index:1000',
        'display:flex',
        'align-items:center',
        'justify-content:center',
        'line-height:1'
    ].join(';');
    document.body.appendChild(btn);

    window.addEventListener('scroll', function () {
        btn.style.opacity = window.scrollY > 300 ? '1' : '0';
        btn.style.pointerEvents = window.scrollY > 300 ? 'auto' : 'none';
    });

    btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
})();
