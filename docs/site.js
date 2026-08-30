document.documentElement.classList.add("js");

async function copyText(button, text) {
  const original = button.textContent;

  try {
    await navigator.clipboard.writeText(text.trim());
    button.textContent = "Copied";
  } catch {
    button.textContent = "Select + copy";
  }

  window.setTimeout(() => {
    button.textContent = original;
  }, 1800);
}

document.querySelectorAll("[data-copy-target]").forEach((button) => {
  button.addEventListener("click", () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (target) copyText(button, target.textContent);
  });
});

document.querySelectorAll("[data-copy-text]").forEach((button) => {
  button.addEventListener("click", () => {
    const label = button.querySelector("em");
    copyText(label || button, button.dataset.copyText);
  });
});
