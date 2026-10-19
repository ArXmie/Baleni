function e(){if(!document.getElementById(`price-pulse-style`)){let e=document.createElement(`style`);e.id=`price-pulse-style`,e.textContent=`
      @keyframes pricePulse {
        0%   { transform: scale(1);    color: inherit; }
        40%  { transform: scale(1.18); color: #bb1414; }
        70%  { transform: scale(0.96); color: #bb1414; }
        100% { transform: scale(1);    color: inherit; }
      }
      .price-animated {
        display: inline-block;
        animation: pricePulse 0.7s ease forwards;
      }
    `,document.head.appendChild(e)}document.querySelectorAll(`.price`).forEach((e,t)=>{setTimeout(()=>{e.classList.add(`price-animated`),e.addEventListener(`animationend`,()=>{e.classList.remove(`price-animated`)},{once:!0})},t*120)})}export{e as t};