(() => {
  function addAccessibleNames() {
    document
      .querySelectorAll('[data-md-component="search"][role="dialog"]:not([aria-label])')
      .forEach((dialog) => dialog.setAttribute("aria-label", "Site search"));

    document
      .querySelectorAll("li.task-list-item input[type=checkbox]:not([aria-label])")
      .forEach((checkbox) => {
        const itemText = checkbox.closest("li.task-list-item")?.textContent?.replace(/\s+/g, " ").trim();
        if (itemText) {
          const status = checkbox.checked ? "Complete" : "Incomplete";
          checkbox.setAttribute("aria-label", `${status} task: ${itemText}`);
        }
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addAccessibleNames, { once: true });
  } else {
    addAccessibleNames();
  }
})();
