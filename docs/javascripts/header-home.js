(() => {
  const title = document.querySelector('.md-header__title');
  const logo = document.querySelector('.md-header__button.md-logo');
  if (!title || !logo) return;

  const link = document.createElement('a');
  link.href = logo.href;
  link.className = 'header-home';
  link.setAttribute('aria-label', 'Cyber Security Learning Platform home');
  while (title.firstChild) link.appendChild(title.firstChild);
  title.appendChild(link);
})();
