let quizzesList = document.querySelector(".quizzes-list");
let questionList = document.querySelector(".questions-list");
let dropdownBtn = document.querySelector(".edit-profile");

function addClass(element, newClass) {
    element.classList.add(newClass);
}

function removeClass(element, newClass) {
    element.classList.remove(newClass);
}

function xorClass(element, newClass) {
    if (element.classList.contains(newClass)) {
        removeClass(element, newClass);
    } else {
        addClass(element, newClass);
    }
}

function checkForExtraContent(container, shadowPlace) {
    if (container == null) return;
    if (container.offsetHeight + container.scrollTop >= container.scrollHeight - 30) {
        removeClass(document.querySelector(shadowPlace), "shadow-above");
    } else {
        addClass(document.querySelector(shadowPlace), "shadow-above");
    }
}

checkForExtraContent(quizzesList, ".add-quiz");
checkForExtraContent(questionList, ".add-question");
document.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
});

function createSection(name, newClass) {
    let ret = document.createElement(name);
    ret.className = newClass;
    return ret;
}

function addCollapsibleEvent(child) {
    child.addEventListener("click", function () {
        xorClass(this, "rotate");
        this.classList.toggle("active");
        let content = ((this.parentElement).parentElement).lastElementChild;
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
        checkForExtraContent(questionList, ".add-question");
    });
    return child;
}

function createOption(Letter, correct, option) {
    let child1 = createSection("div", "option");
    let child2 = createSection("div", "letter plain-text");
    child2.addEventListener("click", function () {
        let content = this.parentElement;
        content = content.parentElement;
        NodeList.prototype.forEach = Array.prototype.forEach;
        let children = content.childNodes;
        children.forEach(function (item) {
            if (item.nodeName.toLowerCase() == 'div') {
                item.childNodes[0].classList.remove("correct-answer");
            }
        });
        this.classList.add("correct-answer");
    });
    if (correct) {
        child2.className = "letter plain-text correct-answer";
    }
    child2.appendChild(document.createTextNode(Letter));
    let child3 = document.createElement("div");
    child3.className = "option-statement";
    child3.addEventListener("keypress", function () {
        let content = (this.parentElement).parentElement;
        content.style.maxHeight = "100%";
    });
    child3.contentEditable = "true";
    child3.appendChild(document.createTextNode(option));
    child1.appendChild(child2);
    child1.appendChild(child3);
    return child1;
}

function addDeleteEvent(child) {
    child.addEventListener("click", function () {
        this.classList.toggle("active");
        let content = (this.parentElement).parentElement;
        if (confirm("Are you sure you want to delete this question?")) {
            fetch('/workspace', {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'DELETE',
                body: JSON.stringify({
                    'question': content,
                    'object_to_delete': 'question',
                })
            });
            content.parentNode.removeChild(content);
            checkForExtraContent(questionList, ".add-question");
        }
    });
    return child;
}

function addDeleteQuizEvent(child) {
    child.addEventListener("click", function () {
       
        let content = (child.parentElement).parentElement;
        let id = (content.firstElementChild).href,tmp="";
        for (let i=id.length-1;i>=0;i--){
            if (id.charAt(i)=="=")break;
            tmp+=id.charAt(i);
        }
        id = tmp.split("").reverse().join("");
        if (confirm("Are you sure you want to delete this quiz?")){
            // do the backend
            var data = { type: "DELETE_QUIZ", text: id };
            window.postMessage(data, "*");
            content.parentNode.removeChild(content);
            checkForExtraContent(quizzesList, ".add-quiz");
        }
    });
    return child;
}

function createQuestionElement(questionStatement, option1, option2, option3, option4) {
    let node = createSection("div", "question_1");
    let panel = createSection("div", "question-panel flex-center");
    let child1 = createSection("div", "question-statement");
    child1.contentEditable = "true";
    child1.appendChild(document.createTextNode(questionStatement));
    panel.appendChild(child1);
    child1 = createSection("button", "icon delete-question");
    child1 = addDeleteEvent(child1);
    let child2 = createSection("i", "fa fa-trash");
    child1.appendChild(child2);
    panel.appendChild(child1);
    child1 = createSection("button", "icon expand-icon collapsible");
    child1 = addCollapsibleEvent(child1);
    child2 = createSection("i", "fa fa-angle-down");
    child1.appendChild(child2);
    panel.appendChild(child1);
    node.appendChild(panel);
    panel = createSection("div", "options-container");
    let options = [option1, option2, option3, option4];
    let chars = ["A", "B", "C", "D"];
    for (let i = 0; i < options.length; i++) {
        child1 = createOption(chars[i], (id == i), options[i]);
        panel.appendChild(child1);
    }
    node.appendChild(panel);
    return node;
}

quizzesList.addEventListener('scroll', function () {
    checkForExtraContent(quizzesList, ".add-quiz");
});
if (questionList != null)
    questionList.addEventListener('scroll', function () {
        checkForExtraContent(questionList, ".add-question");
    });

function isNumber(char) {
    if (typeof char !== 'string') {
        return false;
    }

    if (char.trim() === '') {
        return false;
    }

    return !isNaN(char);
}

function QREvent(child) {
    child.classList.toggle("active");
    let quiz = (child.parentElement).parentElement;
    quiz = (quiz.firstElementChild);
    let qr = document.querySelector(".prompt3");
    qr.classList.add("prompt3--show");
    let quizLink = quiz.href;
    let quizId = "";
    for (let i = quizLink.length - 1; i >= 0; i--) {
        if (isNumber(quizLink[i])) {
            quizId += quizLink.charAt(i);
        } else break;
    }
    quizId = quizId.split("").reverse().join("");
    qr.querySelector(".prompt-text").textContent = "Quiz ID : " + quizId;

    let parametersJson = {
        "size": 300, // Size of Qr Code
        "backgroundColor": "19-80-93", // Background Color Of Qr Code (In RGB)
        "qrColor": "255-255-255", // Color of Qr Code (In RGB)
        "padding": 2, // Padding 
        "data": "dev.to"
    };

    let parameters;
    let img = document.querySelector(".prompt3 img");
    img.addEventListener("click", function () {
        window.location.href = "/quiz/" + quizId;
    });
    parametersJson.data = window.location.hostname + "/invited/" + quizId;
    parameters = `size=${parametersJson.size}&bgcolor=${parametersJson.backgroundColor}&color=${parametersJson.qrColor}&qzone=${parametersJson.padding}&data=${parametersJson.data}`; // Stitch Together all Paramenters
    img.src = `https://api.qrserver.com/v1/create-qr-code/?${parameters}`;
    return child;
}

/* global helpers*/

dropdownBtn.addEventListener("click", function () {
    xorClass(document.querySelector(".dropdown-menu"), "show-menu");
});

function updateLisners() {
    Array.from(document.getElementsByClassName("collapsible")).forEach(element=>{
        element.addEventListener("click", function () {
        xorClass(this, "rotate");
        this.classList.toggle("active");
        let content = (this.parentElement).parentElement;
        content = content.lastElementChild;
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
        });
    });
    Array.from(document.getElementsByClassName("delete-quiz")).forEach(element=>{
        addDeleteQuizEvent(element);
    });
    Array.from(document.getElementsByClassName("share-quiz")).forEach(element=>{
        element.addEventListener("click", function () {
            QREvent(this);
        });
    });
    Array.from(document.getElementsByClassName("delete-question")).forEach(element=>{
        addDeleteEvent(element);
    });
    Array.from(document.getElementsByClassName("expand-icon")).forEach(element=>{
        element.addEventListener("click", function () {
            this.classList.toggle("active");
            let content = (this.parentElement).parentElement;
            content = content.lastElementChild;
            xorClass(content, "add-border");
        });
    });
    Array.from(document.getElementsByClassName("option-statement")).forEach(element=>{
        element.addEventListener("keydown", function () {
            let content = this.parentElement;
            content = content.parentElement;
            content.style.maxHeight = "100%";
        });
    });
    Array.from(document.getElementsByClassName("letter")).forEach(element=>{
        element.addEventListener('click', function () {
            let content = this.parentElement;
            content = content.parentElement;
            NodeList.prototype.forEach = Array.prototype.forEach;
            let children = content.childNodes;
            children.forEach(function (item) {
                if (item.nodeName.toLowerCase() === 'div') {
                    item.childNodes[0].classList.remove("correct-answer");
                }
            });
            this.classList.add("correct-answer");
        });
    });
}

updateLisners();


let id = -1;
let showPrompt2 = (function () {

    let promptEl = document.querySelector('.prompt2'), _cb = null;

    let prompt = {
        el: promptEl,
        form: promptEl.querySelector('.prompt-form2'),
        text: promptEl.querySelector('.prompt-text'),
        input: promptEl.querySelectorAll('.prompt-input'),
        submit: promptEl.querySelector('.prompt-submit')
    };

    prompt.form.addEventListener('submit', hide, false);

    function show(text, cb) {
        prompt.el.classList.add('prompt2--show');
        prompt.text.innerHTML = text;
        _cb = cb;
    }

    function hide(e) {
        let ok = true;
        id = -1;
        for (let i = 0; i < prompt.input.length; i++) {
            let option = prompt.input[i].parentElement;
            option = option.parentElement;
            option = option.firstChild;
            if (prompt.input[i].value == "") {
                ok = false;
            }
            if (i > 0 && option.classList.contains("correct-answer")) {
                id = i - 1;
            }
        }
        e.preventDefault();
        if (!ok) {
            alert("Please fill all required field");
        } else if (id == -1) {
            alert("Please check the correct answer by clicking on its letter");
        } else {
            prompt.el.classList.remove('prompt2--show');
            _cb.call(prompt, prompt.input[0].value, prompt.input[1].value, prompt.input[2].value, prompt.input[3].value, prompt.input[4].value);
            let inpuVals = document.querySelectorAll(".prompt2 .input-field input");
            let options = document.querySelectorAll(".prompt2 .letter");
            Array.from(inpuVals).forEach(element=>{
                element.value = "";
            });
            Array.from(options).forEach(element=>{
                element.classList.remove("correct-answer");
            });
        }
    }

    return show;
})();

let showPrompt = (function () {

    let promptEl = document.querySelector('.prompt'),
        _cb = null;

    let prompt = {
        el: promptEl,
        form: promptEl.querySelector('.prompt-form'),
        text: promptEl.querySelector('.prompt-text'),
        input: promptEl.querySelector('.prompt-input'),
        submit: promptEl.querySelector('.prompt-submit')
    };

    prompt.form.addEventListener('submit', hide, false);

    function show(text, cb) {
        prompt.el.classList.add('prompt--show');
        prompt.text.innerHTML = text;
        _cb = cb;
    }

    function hide(e) {
        e.preventDefault();
        if (prompt.input.value == "") {
            alert("Please fill all required field");
        } else {
            prompt.el.classList.remove('prompt--show');
            _cb.call(prompt, prompt.input.value);
            let inpuVals = document.querySelectorAll(".prompt .input-field input");
            Array.from(inpuVals).forEach(element=>{
                element.value = "";
            });
        }
    }


    return show;

})();


let addQuiz = document.querySelector(".add-quiz");
addQuiz.addEventListener('click', function () {
    let quizName = "";
    showPrompt('You need to provide your quiz name to continue!', function (answer) {
        quizName = answer;
        if (quizName != "") {
            createNewQuiz(quizName);
        }
    });
});

document.querySelector(".prompt-cancel").addEventListener('click', function () {
    document.querySelector('.prompt').classList.remove('prompt--show');
});
document.querySelector(".prompt-cancel2").addEventListener('click', function () {
    document.querySelector('.prompt2').classList.remove('prompt2--show');
});

let addQuestion = document.querySelector(".add-question");
if (addQuestion != null)
    addQuestion.addEventListener('click', function () {
        showPrompt2('You need to provide information about the question to continue!', function (questionName, option1, option2, option3, option4) {
            if (questionName != "") {
                createNewQuestion(questionName, option1, option2, option3, option4);
            }
        });
    });

function getId() {
    return fetch('/api/get_quizzes_from_user', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'GET'
    }).then((response) => response.json())
        .then((responseData) => {
            return responseData;
        })
        .catch(function (error) {
            console.log(error);
        });
}

async function createNewQuiz(quizName) {
    fetch('/workspace', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({
            'quiz_name': quizName,
        })
    }).then(function () {
        getId().then(function (response) {
            let node = createSection("div", "previous-quiz quiz-1");
            let child1 = document.createElement("div");
            let child2 = document.createElement("a");
            child2.setAttribute("id","go_to_previous_quiz");
            child2.href = "workspace?id=" + response['id'];
            child1.appendChild(document.createTextNode(quizName));
            child2.appendChild(child1);
            node.appendChild(child2);
            child1 = createSection("div", "icons-container");
            child2 = createSection("button", "share-quiz icon");
            child2.addEventListener("click", function () {
                QREvent(this);
            });
            let child3 = createSection("i", "fa fa-share");
            let child4;
            child2.append(child3);
            child1.append(child2);
            child3 = createSection("button", "delete-quiz icon");
            child3 = addDeleteQuizEvent(child3)
            child4 = createSection("i", "fa fa-trash");
            child3.appendChild(child4);
            child1.append(child3);
            node.append(child1);
            let quizzes = document.querySelector(".quizzes-list");
            // wait for the child2.href
            var data = { type: "ADD_QUIZ", text: response['id'] + "~" + quizName };
            window.postMessage(data, "*");
            quizzes.insertBefore(node, addQuiz);
        });

    })
        .catch(function (error) {
            console.log(error);
        });

}


function createNewQuestion(questionStatement, option1, option2, option3, option4) {
    fetch('/workspace', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({
            'question': questionStatement,
            'option_A': option1,
            'option_B': option2,
            'option_C': option3,
            'option_D': option4,
            'right_option': id,
        })
    }).then(function (response) {
        if (response.ok) {
            response.json()
                .then(function (response2) {
                    console.log(response2);
                });
        } else {
            throw Error('Something went wrong');
        }
    })
        .catch(function (error) {
            console.log(error);
        });
    let questionsList = document.querySelector(".questions-list");
    questionsList.insertBefore(createQuestionElement(questionStatement, option1, option2, option3, option4), addQuestion);
}


let slider = document.querySelector(".switch input");
if (slider != null)
    slider.addEventListener("click", function () {
        xorClass((this.parentElement).lastElementChild, "slider-clicked");
        let sliderState = document.querySelector(".slider").classList.contains('slider-clicked');
        fetch('/workspace', {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'PUT',
            body: JSON.stringify({
                'state': sliderState,
            })
        });
    });

let exitSharing = document.querySelector(".exit-icon");
exitSharing.addEventListener("click", function () {
    let qr = document.querySelector(".prompt3");
    qr.classList.remove("prompt3--show");
});

let logoutBtn = document.querySelector(".dropdown-menu a");
logoutBtn.addEventListener("click",function(){
    var data = { type: "LOGOUT", text: "" };
    window.postMessage(data, "*");
});


let menuBtn = document.querySelector('.menu-btn');
let menu = document.querySelector('.left-side');
menuBtn.addEventListener('click', function() {
    menu.classList.toggle('active');
});

let show_result = document.getElementById("show-result");
let qr_code = document.getElementById("qr-code");


show_result.addEventListener('click', () => {
    document.getElementById("table-top").style.display = "block";
    document.getElementById("img-container").style.display = "none";
    show_result.style.display = "none";
    qr_code.style.display = "block";
})


qr_code.addEventListener('click', () => {
    document.getElementById("img-container").style.display = "flex"
    document.getElementById("table-top").style.display = "none";
    show_result.style.display = "block";
    qr_code.style.display = "none";
})