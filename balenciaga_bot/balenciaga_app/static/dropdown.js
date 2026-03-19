function toggleDropdown() {
    document.getElementById('dropdown').classList.toggle('open');
  }
  
  document.addEventListener('click', function(e) {
    const dd = document.getElementById('dropdown');
    const av = document.querySelector('.user-avatar');
    if (dd && av && !av.contains(e.target) && !dd.contains(e.target)) {
      dd.classList.remove('open');
    }
  });