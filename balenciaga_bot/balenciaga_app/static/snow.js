(function () {
    var canvas = document.createElement('canvas');
    canvas.id = 'snow-canvas';
    canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 0;
    `;
    document.body.insertBefore(canvas, document.body.firstChild);

    var ctx = canvas.getContext('2d');
    var raindrops = [];
    var COUNT = 120;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    resize();
    window.addEventListener('resize', resize);

    for (var i = 0; i < COUNT; i++) {
        raindrops.push({
            x:       Math.random() * canvas.width,
            y:       Math.random() * canvas.height,
            length:  Math.random() * 20 + 5,
            speed:   Math.random() * 8 + 9,
            drift:   2 - 0.6,
            opacity: Math.random() * 1 + 0.1
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        raindrops.forEach(function (d) {
            var grad = ctx.createLinearGradient(
                d.x, d.y, 
                d.x + d.drift, 
                d.y + d.length
            );
            grad.addColorStop(0, `rgba(0,0,0,${d.opacity})`);
            grad.addColorStop(1, `rgba(0,0,0,${d.opacity * 0.2})`);

            ctx.beginPath();
            ctx.moveTo(d.x, d.y);
            ctx.lineTo(d.x + d.drift, d.y + d.length);
            ctx.lineWidth = 1.2;
            ctx.strokeStyle = grad;
            ctx.stroke();

            d.y += d.speed;
            d.x += d.drift * 0.6;

            if (d.y > canvas.height + d.length) {
                d.y = -d.length;
                d.x = Math.random() * canvas.width;   
            }

            if (d.x > canvas.width + 30)  d.x = -30;
            if (d.x < -30)                d.x = canvas.width + 30;
        });

        requestAnimationFrame(draw);
    }

    draw();
})();