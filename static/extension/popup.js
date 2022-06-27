import {getActiveTabURL} from "./utils.js";

let quizzes = document.querySelectorAll(".share-quiz");
for (let i=0;i<quizzes.length;i++){
    console.log(quizzes[i]);
    quizzes[i].addEventListener("click",async function(){
        let activeTab = await getActiveTabURL();
        chrome.tabs.sendMessage(activeTab.id,{
            type: "SHARE",
            value: quizzes[i].id
        })
    })
}

document.addEventListener("DOMContentLoaded", async function(){
    let quiz = "";
    chrome.storage.sync.get([quiz], (data) => {
        const currentQuizzes = data[quiz] ? JSON.parse(data[quiz]) : [];
        viewQuizzes(currentQuizzes);        
    });
});

const viewQuizzes = (currentQuizzes=[]) => {
    let quizzesList = document.querySelector(".quizzes-container");
    if (currentQuizzes.length > 0) {
      for (let i = 0; i < currentQuizzes.length; i++) {
        addNewQuiz(quizzesList,currentQuizzes[i]);
      }
    }
    return;
};


async function addNewQuiz(quizzesList, newQuiz){
    let quizContainer = document.createElement("div");
    quizContainer.className = "previous-quiz";
    let quizTitle = document.createElement("a");
    quizTitle.textContent = newQuiz.title;
    let iconContainer = document.createElement("div");
    iconContainer.className = "icons-container";
    let shareQuizBtn = document.createElement("button");
    shareQuizBtn.className = "share-quiz icon";
    let activeTab = await getActiveTabURL();
    shareQuizBtn.addEventListener("click",async function(){
        await chrome.tabs.sendMessage(activeTab.id, {
            type: "SHARE",
            value: newQuiz.id,
        });
        window.close();
    });

    let shareIcon = document.createElement("i");
    shareIcon.className = "fa fa-share";
    shareQuizBtn.appendChild(shareIcon);
    iconContainer.appendChild(shareQuizBtn);
    quizContainer.appendChild(quizTitle);
    quizContainer.appendChild(iconContainer);

    quizzesList.appendChild(quizContainer);
};
