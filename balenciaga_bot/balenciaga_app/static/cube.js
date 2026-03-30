(function() {
        const cube = document.getElementById('cube');
        let angleX = 0;
        let angleY = 0;
        let paused = false;

        cube.addEventListener('mouseenter', () => paused = true);
        cube.addEventListener('mouseleave', () => paused = false);

        function tick() {
          if (!paused) {
            angleX += 0.4;
            angleY += 0.6;
          }
          cube.style.transform =
            'rotateX(' + angleX + 'deg) rotateY(' + angleY + 'deg)';
          requestAnimationFrame(tick);
        }
        tick();
      })();