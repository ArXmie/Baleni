export function useProductHover() {
  document.querySelectorAll('.product').forEach((card) => {
    card.style.transition = 'transform 0.25s ease, box-shadow 0.25s ease'
    card.onmouseenter = () => {
      card.style.transform = 'translateY(-6px) scale(1.03)'
      card.style.boxShadow = '0 12px 32px rgba(0,0,0,0.18)'
    }
    card.onmouseleave = () => {
      card.style.transform = 'translateY(0) scale(1)'
      card.style.boxShadow = 'none'
    }
  })
}