
let profile_pic = document.querySelector(".profile-container");
let dropdown_btn = document.querySelector(".edit-profile");
let menu_dropped = false;
dropdown_btn.addEventListener("click",function(){
  let menu = document.querySelector(".dropdown-menu");
  if (menu_dropped == false){
    menu.classList.add("show-menu");
    menu_dropped=true;
    }
  else {
    menu.classList.remove("show-menu");
    menu_dropped=false;
  }
})

// this funciton is too slow I will optimise it
let ending_id = [-1,-1,-1,-1,-1,-1];
function updateLisners(){
  let coll = document.getElementsByClassName("collapsible");
  let j=0;
  for (let i = ending_id[j]; i < coll.length; i++) {
    if (i>ending_id[j]){
      coll[i].addEventListener("click", function() {
        if (this.classList.contains("rotate")){
          this.classList.remove("rotate");
        }
        else {
          this.classList.add("rotate");
        }
        this.classList.toggle("active");
        var content = this.parentElement;
        content = content.parentElement;
        content = content.lastElementChild;
        if (content.style.maxHeight){
          content.style.maxHeight = null;
        } else {
          content.style.maxHeight = content.scrollHeight + "px";
          
        }
      });
      ending_id[j]=i;
    }
  }
  j++;
  let delete_quiz = document.getElementsByClassName("delete-quiz");
  for (let i = ending_id[j]; i<delete_quiz.length;i++){
    if (i>ending_id[j]){

      delete_quiz[i].addEventListener("click",function(){
        this.classList.toggle("active");
        let content = this.parentElement;
        content = content.parentElement;
        if (confirm("Are you sure you want to delete this quiz?")){
          content.parentNode.removeChild(content);
          checkForExtraQuiz();
        }
      });
      ending_id[j]=i;
    }
  }
  j++;
  let delete_question = document.getElementsByClassName("delete-question");
  for (let i = ending_id[j]; i < delete_question.length; i++) {
    if (i>ending_id[j]){

      delete_question[i].addEventListener("click", function() {
        this.classList.toggle("active");
        let content = this.parentElement;
        content = content.parentElement;
        if (confirm("Are you sure you want to delete this question?")){
          content.parentNode.removeChild(content);
          checkForExtraQuestions();
        }
      });
      ending_id[j]=i;
    }
  }
  j++;
  let expan_icon = document.getElementsByClassName("expand-icon");

  for (let i = ending_id[j]; i < expan_icon.length; i++) {
    if (i>ending_id[j]){
      
      expan_icon[i].addEventListener("click", function() {
        this.classList.toggle("active");
        let content = this.parentElement;
        content = content.parentElement;
        content = content.lastElementChild;
        if (content.classList.contains("add-border") == false){
          content.classList.add("add-border");
          checkForExtraQuestions();
        }
        else {
          content.classList.remove("add-border");
          checkForExtraQuestions();
        }
        checkForExtraQuestions();
        ending_id[j]=i;
      });
    }
  }
  j++;
  let editable_text = document.getElementsByClassName("option-statement");
  for (let i = ending_id[j]; i < editable_text.length; i++) {
    if (i>ending_id[j]){

      editable_text[i].addEventListener("keydown", function() {
        let content = this.parentElement;
        content = content.parentElement;
        content.style.maxHeight = "100%";
        content.style.height = "100%";
      });
      ending_id[j]=i;
    }
  }
  j++;
  let options = document.getElementsByClassName("letter");
  for (let i = ending_id[j] ; i < options.length;i++){
    if (i>ending_id[j]){
      options[i].addEventListener('click',function(){
        let content = this.parentElement;
        content = content.parentElement;
        NodeList.prototype.forEach = Array.prototype.forEach
        var children = content.childNodes;
        children.forEach(function(item){
          if (item.nodeName.toLowerCase() == 'div'){
            item.childNodes[0].classList.remove("correct-answer");
          }
        });
        this.classList.add("correct-answer");
      });
      ending_id[j]=i;
    }
  }
}

updateLisners();

function isOverflownY(element) {
  return element.scrollHeight > element.clientHeight;
}

let quizzes_list = document.querySelector(".quizzes-list");
let shadow_exist_2 = false;
if (isOverflownY(quizzes_list) == true){
  let add_quiz = document.querySelector(".add-quiz");
  add_quiz.classList.add("shadow-above");
  shadow_exist_2 = true;
}
function checkForExtraQuiz(){
  if (quizzes_list.offsetHeight + quizzes_list.scrollTop >= quizzes_list.scrollHeight - 30 ){
    if (shadow_exist_2 == true){
      let add_quiz = document.querySelector(".add-quiz");
      add_quiz.classList.remove("shadow-above");
      shadow_exist_2 = true;
    }
  }
  else{
    if (shadow_exist_2 == false){
      let add_quiz = document.querySelector(".add-quiz");
      add_quiz.classList.add("shadow-above");
      shadow_exist_2 = true;
    }
  }
}

quizzes_list.addEventListener('scroll',function(){
  checkForExtraQuiz();
});

let question_list = document.querySelector(".questions-list");
let shadow_exist = false;

if (isOverflownY(question_list) == true){
  let add_question = document.querySelector(".add-question");
  add_question.classList.add("shadow-above");
  shadow_exist = true;
}


function checkForExtraQuestions(){
  if (question_list.offsetHeight + question_list.scrollTop >= question_list.scrollHeight - 30 ){
    let add_question = document.querySelector(".add-question");
    if (add_question.classList.contains("shadow-above") == true){
      add_question.classList.remove("shadow-above");
      shadow_exist = false;
    }
  }
  else {
    let add_question = document.querySelector(".add-question");
    if (add_question.classList.contains("shadow-above")  == false){
      add_question.classList.add("shadow-above");
      shadow_exist = true;
    }
  }
}

question_list.addEventListener('scroll',function(){
  checkForExtraQuestions();
});


document.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    document.execCommand('insertLineBreak');
    event.preventDefault();
  }
})



let add_quiz = document.querySelector(".add-quiz");
let add_question = document.querySelector(".add-question");
let id=-1;
let showPrompt2 =  (function(){
  
  let promptEl = document.querySelector('.prompt2'),
    _cb = null;
  
  let prompt = {
    el: promptEl,
    form: promptEl.querySelector('.prompt__form2'),
    text: promptEl.querySelector('.prompt__text'),
    input: promptEl.querySelectorAll('.prompt__input'),
    submit: promptEl.querySelector('.prompt__submit')
  }
  
  prompt.form.addEventListener('submit', hide, false);

  function show( text, cb ){
    prompt.el.classList.add('prompt2--show');
    prompt.text.innerHTML = text;
    _cb = cb;
  }

  function hide( e ){
    let ok=true;
    id=-1;
    for (let i=0;i<prompt.input.length;i++){
      let option = prompt.input[i].parentElement;
      option = option.parentElement;
      option = option.firstChild;
      if (prompt.input[i].value == ""){
        ok=false;
      }
      if (i>0 && option.classList.contains("correct-answer")==true){
        id=i-1;
      }
    }
    
    e.preventDefault();
    if (ok==false){
      alert("Please fill all required field");
    }
    else if (id==-1){
      alert("Please check the correct answer by clicking on its letter")
    }
    else {
      prompt.el.classList.remove('prompt2--show');
      _cb.call( prompt, prompt.input[0].value,prompt.input[1].value,prompt.input[2].value,prompt.input[3].value,prompt.input[4].value );
      let inpu_vals = document.querySelectorAll(".prompt2 .input-field input");
      let options = document.querySelectorAll(".prompt2 .letter");
      for (let i=0;i<inpu_vals.length;i++){
        inpu_vals[i].value="";
      }
      for (let i=0;i<options.length;i++){
        options[i].classList.remove("correct-answer");
      }
    }
  }
  
  return show;
  
})();

let showPrompt = (function(){
  
  let promptEl = document.querySelector('.prompt'),
    _cb = null;
  
  let prompt = {
    el: promptEl,
    form: promptEl.querySelector('.prompt__form'),
    text: promptEl.querySelector('.prompt__text'),
    input: promptEl.querySelector('.prompt__input'),
    submit: promptEl.querySelector('.prompt__submit')
  }
  
  prompt.form.addEventListener('submit', hide, false);

  function show( text, cb ){
    prompt.el.classList.add('prompt--show');
    prompt.text.innerHTML = text;
    _cb = cb;
  }

  function hide( e ){
    e.preventDefault();
    if (prompt.input.value == ""){
      alert("Please fill all required field");
    }
    else {
      prompt.el.classList.remove('prompt--show');
      _cb.call( prompt, prompt.input.value );
      let inpu_vals = document.querySelectorAll(".prompt .input-field input")
      for (let i=0;i<inpu_vals.length;i++){
        inpu_vals[i].value="";
      }
    }
  }
  
  
  return show;
  
})();

add_quiz.addEventListener('click',function(){
  let quiz_name = "";
  showPrompt('You need to provide your quiz name to continue!', function( answer ){
    quiz_name = answer;
    if (quiz_name!=""){
      createNewQuiz(quiz_name);
    }
  });  
})

let prompt__cancel = document.querySelector(".prompt__cancel");
prompt__cancel.addEventListener('click',function(){
  let promptEl = document.querySelector('.prompt');
  promptEl.classList.remove('prompt--show');
});

let prompt__cancel2 = document.querySelector(".prompt__cancel2");
prompt__cancel2.addEventListener('click',function(){
  let promptEl = document.querySelector('.prompt2');
  promptEl.classList.remove('prompt2--show');
});


add_question.addEventListener('click',function(){
  showPrompt2('You need to provide information about the question to continue!', function(question_name,option_1,option_2,option_3,option_4){
    if (question_name!=""){
      createNewQuestion(question_name,option_1,option_2,option_3,option_4);
    }
  });  
});

function createNewQuiz(quiz_name){
  let node = document.createElement("div");
  node.className="previous-quiz quiz-1";
  let child1 = document.createElement("div");
  let child2 = document.createElement("a");
  child2.href = "#";
  child2.appendChild(document.createTextNode(quiz_name));
  child1.appendChild(child2);
  node.appendChild(child1);

  child1 = document.createElement("div");
  child1.className="icons-container";

  child2 = document.createElement("label");
  child2.className="switch";
  
  let child3 = document.createElement("input");
  let child4 = document.createElement("span");
  child4.className="slider";
  child3.type="checkbox";
  
  child2.append(child3);
  child2.append(child4);

  child1.append(child2);
  node.append(child1);

  child1 = document.createElement("button");
  child1.className = "delete-quiz icon";

  child2 = document.createElement("i");
  child2.className = "fa fa-trash";

  child1.appendChild(child2);

  node.append(child1);
  let quizzes = document.querySelector(".quizzes-list");
  quizzes.insertBefore(node,add_quiz);
  updateLisners();
}


function createNewQuestion(questoin_statement, option_1,option_2,option_3,option_4){
  let add_question = document.querySelector(".add-question");
  let node = document.createElement("div");
  node.className = "question_1";

  let panel = document.createElement("div");
  panel.className =  "question-panel flex-center";

  let child1 = document.createElement("div");
  child1.classList = "question-statement";
  child1.contentEditable = "true";
  child1.appendChild(document.createTextNode(questoin_statement));
  panel.appendChild(child1);

  child1 = document.createElement("button");
  child1.className = "icon delete-question";
  let child2 = document.createElement("i");
  child2.className = "fa fa-trash";
  child1.appendChild(child2);
  panel.appendChild(child1);

  child1 = document.createElement("button");
  child1.className = "icon expand-icon collapsible";
  child2 = document.createElement("i");
  child2.className = "fa fa-angle-down";
  child1.appendChild(child2);
  panel.appendChild(child1);

  node.appendChild(panel);

  panel = document.createElement("div");
  panel.className = "options-container";

  child1 = document.createElement("div");
  child1.className = "option";
  child2 = document.createElement("div");
  child2.className = "letter plain-text";
  if (id==0){
    child2.className="letter plain-text correct-answer"; 
  }
  child2.appendChild(document.createTextNode("A"));
  let child3 = document.createElement("div");
  child3.className = "option-statement";
  child3.contentEditable = "true";
  child3.appendChild(document.createTextNode(option_1));
  child1.appendChild(child2);
  child1.appendChild(child3);
  panel.appendChild(child1);

  child1 = document.createElement("div");
  child1.className = "option";
  child2 = document.createElement("div");
  child2.className = "letter plain-text";
  if (id==1){
    child2.className="letter plain-text correct-answer"; 
  }
  child2.appendChild(document.createTextNode("B"));
  child3 = document.createElement("div");
  child3.className = "option-statement";
  child3.contentEditable = "true";
  child3.appendChild(document.createTextNode(option_2));
  child1.appendChild(child2);
  child1.appendChild(child3);
  panel.appendChild(child1);

  child1 = document.createElement("div");
  child1.className = "option";
  child2 = document.createElement("div");
  child2.className = "letter plain-text";
  if (id==2){
    child2.className="letter plain-text correct-answer"; 
  }
  child2.appendChild(document.createTextNode("C"));
  child3 = document.createElement("div");
  child3.className = "option-statement";
  child3.contentEditable = "true";
  child3.appendChild(document.createTextNode(option_3));
  child1.appendChild(child2);
  child1.appendChild(child3);
  panel.appendChild(child1);

  child1 = document.createElement("div");
  child1.className = "option";
  child2 = document.createElement("div");
  child2.className = "letter plain-text";
  if (id==3){
    child2.className="letter plain-text correct-answer"; 
  }
  child2.appendChild(document.createTextNode("D"));
  child3 = document.createElement("div");
  child3.className = "option-statement";
  child3.contentEditable = "true";
  child3.appendChild(document.createTextNode(option_4));
  child1.appendChild(child2);
  child1.appendChild(child3);
  panel.appendChild(child1);

  node.appendChild(panel);

  let questions_list = document.querySelector(".questions-list");
  questions_list.insertBefore(node,add_question);
  updateLisners();
}

