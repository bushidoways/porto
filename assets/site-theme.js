(() => {
  if (window.__nangThemeLoaded) return;
  window.__nangThemeLoaded = true;
  const root = document.documentElement;
  const key = 'nang-theme';
  const read = () => { try { return localStorage.getItem(key); } catch { return null; } };
  const apply = value => {
    root.dataset.theme = value === 'malem' ? 'malem' : 'sore';
    document.querySelectorAll('.site-theme-toggle button').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.tset === root.dataset.theme));
    });
  };
  apply(read());
  const init = () => {
    if (document.querySelector('.site-theme-toggle')) return;
    const group = document.createElement('div');
    group.className = 'site-theme-toggle';
    group.setAttribute('role', 'group');
    group.setAttribute('aria-label', 'Tema tampilan');
    for (const [value, label] of [['sore', 'Sore'], ['malem', 'Malam']]) {
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.tset = value;
      button.textContent = label;
      button.addEventListener('click', () => {
        const changed = root.dataset.theme !== value;
        apply(value);
        try { localStorage.setItem(key, value); } catch {}
        if (changed && !matchMedia('(prefers-reduced-motion: reduce)').matches && button.animate) {
          button.animate([{ transform: 'scale(0.9)' }, { transform: 'scale(1.06)' }, { transform: 'scale(1)' }], { duration: 320, easing: 'ease-out' });
        }
      });
      group.append(button);
    }
    document.body.append(group);
    apply(read());
    addEventListener('storage', event => {
      if (event.key === key || event.key === null) apply(read());
    });
    addEventListener('pageshow', () => apply(read()));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
