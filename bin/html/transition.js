document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".section");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");  // add when in view
        } else {
          entry.target.classList.remove("show"); // remove when out of view
        }
      });
    },
    {
      threshold: 0.2 // show when at least 20% of section is visible
    }
  );

  sections.forEach(section => observer.observe(section));
});
