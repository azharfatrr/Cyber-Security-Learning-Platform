(() => {
  const sizes = { small: '0.875', default: '1', large: '1.15', larger: '1.3' };
  let selected = 'default';
  try {
    const saved = localStorage.getItem('lab-content-size');
    if (Object.hasOwn(sizes, saved)) selected = saved;
  } catch (_) { /* The control still works when storage is unavailable. */ }

  const header = document.querySelector('.md-header__inner');
  if (!header) return;
  const label = document.createElement('label');
  label.className = 'text-size-control';
  const icon = document.createElement('span');
  icon.textContent = 'Aa';
  icon.setAttribute('aria-hidden', 'true');
  label.appendChild(icon);
  const select = document.createElement('select');
  select.id = 'text-size';
  select.setAttribute('aria-label', 'Text size');
  for (const [value, text] of [['small', 'Small'], ['default', 'Default'], ['large', 'Large'], ['larger', 'Larger']]) {
    select.add(new Option(text, value));
  }
  select.value = selected;
  label.appendChild(select);
  const search = header.querySelector('label[for="__search"]');
  header.insertBefore(label, search || null);

  const apply = () => {
    document.documentElement.style.setProperty('--content-scale', sizes[select.value] || sizes.default);
  };
  apply();
  select.addEventListener('change', () => {
    apply();
    try { localStorage.setItem('lab-content-size', select.value); } catch (_) { /* Optional preference. */ }
  });
})();
