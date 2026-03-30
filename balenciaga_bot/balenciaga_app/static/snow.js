(function() {
    const canvas = document.getElementById('snow-canvas');
    const ctx = canvas.getContext('2d');
    let raindrops = [];
    const COUNT = 250;

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    for (let i = 0; i < COUNT; i++) {
        raindrops.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            length: Math.random() * 10 + 5,
            speed: Math.random() * 15 + 10,
            drift: Math.random() * 1.5 - 0.75,
            opacity: Math.random() * 0.5 + 0.2
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        raindrops.forEach(d => {
            const gradient = ctx.createLinearGradient(d.x, d.y, d.x + d.drift, d.y + d.length );
            gradient.addColorStop(0, `rgba(0, 0, 0, ${d.opacity})`);
            gradient.addColorStop(1, `rgba(0, 0, 0, ${d.opacity * 0.3})`);
            
            ctx.beginPath();
            ctx.moveTo(d.x, d.y);
            ctx.lineTo(d.x + d.drift, d.y + d.length);
            ctx.lineWidth = 1.5;
            ctx.strokeStyle = gradient;
            ctx.stroke();

            d.y += d.speed;
            d.x += d.drift * 0.8;

            if (d.y > canvas.height + d.length) {
                d.y = -d.length;
                d.x = Math.random() * canvas.width;
                d.speed = Math.random() * 15 + 10;
            }
            if (d.x > canvas.width + 30) d.x = -30;
            if (d.x < -30) d.x = canvas.width + 30;
        });
        
        requestAnimationFrame(draw);
    }
    draw();
})();