(() => {
    let quiz = "";
    let currentQuizzes = [];
    function fetchQuizzes(){
        return new Promise((resolve)=>{
            chrome.storage.sync.get([quiz],(obj)=>{
                resolve(obj[quiz] ? JSON.parse(obj[quiz]):[]);
            })
        })
    }

    async function addNewQuiz(quizId,quizTitle){

        let newQuiz = {
            id: quizId,
            title: quizTitle
        }
        currentQuizzes = await fetchQuizzes();
        let exist = false;
        for (let i=0;i<Array.from(currentQuizzes).length;i++){
            if (currentQuizzes[i].id == newQuiz.id){
                exist=true;
            }
        }
        if (exist==false){
            chrome.storage.sync.set({
                [quiz]: JSON.stringify([...currentQuizzes, newQuiz])
            });
        }
    }

    async function workspace_loaded(){
        let websiteList = document.getElementsByClassName("previous-quiz quiz-1");
        for (let i=0;i<websiteList.length;i++){
            let q = websiteList[i].firstElementChild;
            let link = q.href;
            let tmp = "";
            for (let j=link.length-1;j>=0;j--){
                if (link.charAt(j)=="=")break;
                tmp+=link.charAt(j);
            }
            link = tmp.split("").reverse().join("");
            await addNewQuiz(link,(q.firstElementChild).innerHTML);
        }
    }
    async function deleteQuiz(quizId){
        currentQuizzes = currentQuizzes.filter((b) => b.id != quizId);
        chrome.storage.sync.set({ [quiz]: JSON.stringify(currentQuizzes) });
    }
    window.addEventListener("message", function(event) {
        if (event.source != window)
        return;
        if (event.data.type && (event.data.type == "DELETE_QUIZ")) {
            deleteQuiz(event.data.text);
        }
        if (event.data.type && (event.data.type == "ADD_QUIZ")){
            let id="",title="",isTxt=false;
            for (let i=0;i<event.data.text.length;i++){
                if (event.data.text.charAt(i)=="~"){
                    break;
                }
                id+=event.data.text.charAt(i);
            }
            for (let i=0;i<event.data.text.length;i++){
                if (isTxt){
                    title+=event.data.text.charAt(i);
                }
                if (event.data.text.charAt(i)=="~"){
                    isTxt=true;
                }
            }
            addNewQuiz(id,title);
        }
        if (event.data.type && (event.data.type == "LOGOUT")) {
            currentQuizzes = [];
            chrome.storage.sync.set({ [quiz]: JSON.stringify(currentQuizzes) });
        }
    })
    chrome.runtime.onMessage.addListener((obj,sender,response)=>{
        const { type, value } = obj;
        if (type==="NEW"){
            workspace_loaded();
        }else if (type==="SHARE"){
            let prompt = document.querySelector(".__prompt3");
            prompt.style.visibility = "visible";
            prompt.style.opacity = "1";
            prompt.querySelector(".__prompt-text").textContent = "Quiz ID : " + value;
            let parametersJson = {
                "size": 300, // Size of Qr Code
                "backgroundColor": "19-80-93", // Background Color Of Qr Code (In RGB)
                "qrColor": "255-255-255", // Color of Qr Code (In RGB)
                "padding": 2, // Padding 
                "data": "dev.to"
            };
            let parameters;
            let img = document.querySelector(".__prompt-img");
            parametersJson.data = "http://daber.space" + "/invited/" + value;
            parameters = `size=${parametersJson.size}&bgcolor=${parametersJson.backgroundColor}&color=${parametersJson.qrColor}&qzone=${parametersJson.padding}&data=${parametersJson.data}`; // Stitch Together all Paramenters
            img.src = `https://api.qrserver.com/v1/create-qr-code/?${parameters}`;
        }
    })
})();

let promptInject = document.createElement("div");
promptInject.className = "__prompt3";
promptInject.setAttribute("style","position: fixed;top: 0;left: 0;right: 0;bottom: 0;background: rgba(40, 40, 40, .37);z-index: 1000000;visibility: hidden;opacity: 0;transition: .6s opacity, .6s visibility;text-align: center;margin: auto;font-size: 1.5rem;font-weight: 900;color: #13505D;width: 100vw;height:100vh;");

let child1 = document.createElement("div");
child1.className = "__prompt-container";
child1.setAttribute("style","position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);width: 500px;background: #fff;padding: 1.5rem 3rem 3rem 3rem;border-radius: 1.5rem 0 1.5rem 1.5rem;");
let child2 = document.createElement("div");
child2.className = "__exit-icon";
child2.addEventListener("mouseenter",function(){
    console.log("hi");
    let icon = document.querySelector(".__exit-icon");
    icon.style.color = "#fff";
    icon.style.backgroundColor = "#005F75";
});
child2.addEventListener("mouseleave",function(){
    console.log("hi");
    let icon = document.querySelector(".__exit-icon");
    icon.style.color = "#005F75";
    icon.style.backgroundColor = "#fff";
});
child2.addEventListener("click", function () {
    let prompt = document.querySelector(".__prompt3");
    prompt.style.visibility = "hidden";
    prompt.style.opacity = "0";
});

child2.setAttribute("style","position: absolute;right: 0;top: 0;border-left: #005F75 solid 0.2rem;border-bottom: #005F75 solid 0.2rem;width: 38px;height: 38px;color: #005F75;display: flex;justify-content: center;align-items: center;border-radius: 0 0 0 0.5rem;transition: all 0.3s;cursor: pointer;");
let child3 = document.createElement("div");
child3.textContent = "X";
child3.setAttribute("style","width: 20px;");
child2.appendChild(child3);
child1.appendChild(child2);

child3 = document.createElement("p");
child3.className = "__prompt-text";
child3.setAttribute("style","text-align: center;margin: 1rem auto 2rem auto;font-size: 1.5rem;font-weight: 900;color: #13505D;");
child1.appendChild(child3);

let child4 = document.createElement("div");
child4.className = "__img-container";
child4.setAttribute("style","display: flex;justify-content: center;align-items: center;border-radius: 2rem;")
let child5 = document.createElement("img");
child5.className = "__prompt-img";
child5.setAttribute("style","width: 300px;height: 300px;border-radius: 0.5rem;")
child5.setAttribute("src","");
child4.appendChild(child5);
child1.appendChild(child4);

child1.appendChild(child4);

promptInject.appendChild(child1);

document.body.appendChild(promptInject);