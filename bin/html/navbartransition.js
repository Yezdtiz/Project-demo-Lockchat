document.addEventListener("DOMContentLoaded", () => {
  const navbar = document.querySelector(".navbar");
  if (!navbar) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY < 150) { // 🔹 150px đầu trang
      navbar.classList.add("home-style");
    } else {
      navbar.classList.remove("home-style");
    }
  });

  // check khi load trang
  if (window.scrollY < 160) {
    navbar.classList.add("home-style");
  }
});
