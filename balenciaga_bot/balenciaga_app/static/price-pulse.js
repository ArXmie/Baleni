(function () {
    function init() {
        var prices = document.querySelectorAll('.price');
        if (!prices.length) return;

        var style = document.createElement('style');
        style.textContent = [
            '@keyframes pricePulse {',
            '  0%   { transform: scale(1);    color: inherit; }',
            '  40%  { transform: scale(1.18); color: #bb1414; }',
            '  70%  { transform: scale(0.96); color: #bb1414; }',
            '  100% { transform: scale(1);    color: inherit; }',
            '}',
            '.price-animated {',
            '  display: inline-block;',
            '  animation: pricePulse 0.7s ease forwards;',
            '}'
        ].join('\n');
        document.head.appendChild(style);

        prices.forEach(function (el, i) {
            setTimeout(function () {
                el.classList.add('price-animated');
                el.addEventListener('animationend', function () {
                    el.classList.remove('price-animated');
                }, { once: true });
            }, i * 120);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
