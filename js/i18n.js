// === Hola
//   _-=Created Without Love=- _                   
//  | \ | ___ ._ _  ___  ___
//  |   |<_> || ' |/ . |<_-<
//  |_\_|<___||_|_|\_. |/__/
//                 <___' 
  

(function () {
  'use strict';

  // ==================== CSS INJECTION ====================
  const style = document.createElement('style');
  style.textContent = `
    .lang-toggle {
      display: flex; align-items: center; gap: 6px;
      padding: 4px; background: rgba(19,19,31,0.9);
      border: 1px solid rgba(99,102,241,0.15);
      border-radius: 100px; cursor: pointer;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem; font-weight: 600;
      letter-spacing: 0.04em;
      transition: border-color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      margin-left: auto;
      flex-shrink: 0;
    }
    .lang-toggle:hover { border-color: rgba(99,102,241,0.4); }
    .lang-opt {
      padding: 4px 10px; border-radius: 100px;
      color: rgba(100,116,139,1);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      user-select: none;
    }
    .lang-opt.active {
      color: white;
      background: #6366f1;
    }
  `;
  document.head.appendChild(style);

  // ==================== TOGGLE INJECTION ====================
  const nav = document.querySelector('nav');
  if (!nav) return;

  const toggle = document.createElement('div');
  toggle.className = 'lang-toggle';
  toggle.id = 'langToggle';
  toggle.setAttribute('aria-label', 'Switch language');
  toggle.innerHTML = '<span class="lang-opt active" data-lang="id">ID</span><span class="lang-opt" data-lang="en">EN</span>';

  const navBack = nav.querySelector('.nav-back');
  const hamburgerWrapper = nav.querySelector('.nav-hamburger');
  
  if (navBack) {

    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'display:flex;align-items:center;gap:12px;';
    navBack.parentNode.insertBefore(wrapper, navBack);
    wrapper.appendChild(toggle);
    wrapper.appendChild(navBack);
  } else if (hamburgerWrapper) {

    const hamParent = hamburgerWrapper.parentNode;
    if (hamParent.tagName === 'DIV' && hamParent.parentNode === nav) {
      hamParent.insertBefore(toggle, hamburgerWrapper);
    } else {
      nav.insertBefore(toggle, hamburgerWrapper);
    }
  } else {
    nav.appendChild(toggle);
  }

  
  let currentLang = localStorage.getItem('nang-lang') || 'id';

  function getTranslations() {
    return window.PAGE_TRANSLATIONS || {};
  }

  function setLang(lang) {
    currentLang = lang;
    localStorage.setItem('nang-lang', lang);
    document.documentElement.lang = lang;

    // Update toggle UI
    document.querySelectorAll('.lang-opt').forEach(function (opt) {
      opt.classList.toggle('active', opt.dataset.lang === lang);
    });

    // Apply translations — always read fresh from window
    var t = getTranslations();
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.dataset.i18n;
      if (t[key] && t[key][lang] !== undefined) {
        el.innerHTML = t[key][lang];
      }
    });
  }

  // Click handler
  toggle.addEventListener('click', function (e) {
    var clicked = e.target.closest('.lang-opt');
    if (clicked) {
      setLang(clicked.dataset.lang);
    } else {
      setLang(currentLang === 'id' ? 'en' : 'id');
    }
  });

  // Apply saved language on load
  if (currentLang !== 'id') {
    setLang(currentLang);
  }

  // Expose globally for dynamic use
  window.nangI18n = { setLang: setLang, getLang: function () { return currentLang; } };
})();
