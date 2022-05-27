const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const left_panel_img = document.querySelector(".left-panel");
const right_panel_img = document.querySelector(".right-panel");
const container = document.querySelector(".container");

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});