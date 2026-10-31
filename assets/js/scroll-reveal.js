/* Zhenda Premium — 滚动显现动画
   使用 IntersectionObserver 监听 .z-reveal 元素进入视口时添加 .is-visible
   支持降级: 无 IO 时立即显示全部 */
(function () {
  'use strict';

  var reveals = document.querySelectorAll('.z-reveal');
  if (!reveals.length) return;

  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    rootMargin: '0px 0px -8% 0px',
    threshold: 0.08
  });

  reveals.forEach(function (el) { observer.observe(el); });
})();
