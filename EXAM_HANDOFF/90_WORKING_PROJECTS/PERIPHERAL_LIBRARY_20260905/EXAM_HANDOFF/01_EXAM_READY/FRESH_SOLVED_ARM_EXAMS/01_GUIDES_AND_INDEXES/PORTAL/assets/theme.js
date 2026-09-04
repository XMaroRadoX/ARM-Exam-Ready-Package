/* Apply a local preference before paint; browsing works when storage is blocked. */
(() => {
  document.documentElement.classList.add('js');
  try {
    const value = localStorage.getItem('arm-workstation-theme');
    if (value === 'light' || value === 'dark') document.documentElement.dataset.theme = value;
  } catch (_) { /* System theme remains the default. */ }
})();
