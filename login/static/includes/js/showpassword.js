const togglePassword = document.querySelector("#togglePassword");
const password = document.querySelector("#password");
const form = document.querySelector("form");

togglePassword.addEventListener("click", function () {
  // toggle the type attribute
  const type = password.getAttribute("type") === "password" ? "text" : "password";
  password.setAttribute("type", type);

  // toggle the icon
  this.classList.toggle("bi-eye");
});

form.addEventListener("submit", function () {
  // Enable form submission by removing the event listener
  form.removeEventListener("submit", preventFormSubmit);
});

function preventFormSubmit(e) {
  e.preventDefault();
}
