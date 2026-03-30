(function() {
        const clockEl = document.getElementById('live-clock');
        function tick() {
          const now = new Date();
          const h = String(now.getHours()).padStart(2, '0');
          const m = String(now.getMinutes()).padStart(2, '0');
          const s = String(now.getSeconds()).padStart(2, '0');
          clockEl.textContent = h + ':' + m + ':' + s;
        }
        tick();
        setInterval(tick, 1000);
      })();