const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const left_panel_img = document.querySelector(".left-panel.panel-image");
const right_panel_img = document.querySelector(".right-panel.panel-image");
const container = document.querySelector(".container");

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  sleep(300).then(()=>{
    left_panel.classList.add("hide-panel");
    right_panel.classList.remove("hide-panel");
  });
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  sleep(300).then(()=>{
    left_panel.classList.remove("hide-panel");
    right_panel.classList.add("hide-panel");
  });
});