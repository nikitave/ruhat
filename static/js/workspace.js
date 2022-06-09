/* global helpers*/
let quizzes_list = document.querySelector(".quizzes-list");
let question_list = document.querySelector(".questions-list");
let dropdown_btn = document.querySelector(".edit-profile");
function addClass(element,new_class){
  element.classList.add(new_class);
}
function removeClass(element,new_class){
  element.classList.remove(new_class);
}
function xorClass(element,new_class){
  if (element.classList.contains(new_class) == true){
    removeClass(element,new_class);
  }
  else {
    addClass(element,new_class);
  }
}
function checkForExtraContent(container, shadowPlace){
  if (container.offsetHeight + container.scrollTop >= container.scrollHeight - 30 ){
    removeClass(document.querySelector(shadowPlace),"shadow-above");
  }
  else{
    addClass(document.querySelector(shadowPlace),"shadow-above");
  }
}
checkForExtraContent(quizzes_list,".add-quiz");
checkForExtraContent(question_list,".add-question");
document.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    document.execCommand('insertLineBreak');
    event.preventDefault();
  }
});
function createSection(name,new_class){
  let ret = document.createElement(name);
  ret.className = new_class;
  return ret;
}
function createOption(Letter,correct,option){
  let child1 = createSection("div","option");
  let child2 = createSection("div","letter plain-text");
  if (correct){
    child2.className="letter plain-text correct-answer"; 
  }
  child2.appendChild(document.createTextNode(Letter));
  let child3 = document.createElement("div");
  child3.className = "option-statement";
  child3.contentEditable = "true";
  child3.appendChild(document.createTextNode(option));
  child1.appendChild(child2);
  child1.appendChild(child3);
  return child1;
}
/* global helpers*/

dropdown_btn.addEventListener("click",function(){
  let menu = document.querySelector(".dropdown-menu");
  xorClass(menu,"show-menu");
});

let ending_id = [-1,-1,-1,-1,-1,-1];
function updateLisners(){
  let coll = document.getElementsByClassName("collapsible");
  let j=0;
  for (let i = ending_id[j]+1; i < coll.length; i++) {
      coll[i].addEventListener("click", function() {
        xorClass(this,"rotate");
        this.classList.toggle("active");
        var content = ((this.parentElement).parentElement).lastElementChild;
        if (content.style.maxHeight){
          content.style.maxHeight = null;
        } else {
          content.style.maxHeight = content.scrollHeight + "px";
        }
      });
      ending_id[j]=i;
  }
  j++;

  let delete_quiz = document.getElementsByClassName("delete-quiz");
  for (let i = ending_id[j]+1; i<delete_quiz.length;i++){
    delete_quiz[i].addEventListener("click",function(){
      this.classList.toggle("active");
      let content = (this.parentElement).parentElement;
      if (confirm("Are you sure you want to delete this quiz?")){
        content.parentNode.removeChild(content);
        checkForExtraContent(quizzes_list,".add-quiz");
      }
    });
    ending_id[j]=i;
  }
  j++;
  
  let delete_question = document.getElementsByClassName("delete-question");
  for (let i = ending_id[j]+1; i < delete_question.length; i++) {
    delete_question[i].addEventListener("click", function() {
      this.classList.toggle("active");
      let content = (this.parentElement).parentElement;
      if (confirm("Are you sure you want to delete this question?")){
        content.parentNode.removeChild(content);
        checkForExtraContent(question_list,".add-question");
      }
    });
    ending_id[j]=i;
  }
  j++;

  let expan_icon = document.getElementsByClassName("expand-icon");
  for (let i = ending_id[j]+1; i < expan_icon.length; i++) {
    expan_icon[i].addEventListener("click", function() {
      this.classList.toggle("active");
      let content = ((this.parentElement).parentElement).lastElementChild;
      xorClass(content,"add-border");
      checkForExtraContent(question_list,".add-question");
      ending_id[j]=i;
    });
  }
  j++;

  let editable_text = document.getElementsByClassName("option-statement");
  for (let i = ending_id[j]+1; i < editable_text.length; i++) {
      editable_text[i].addEventListener("keydown", function() {
        let content = this.parentElement;
        content = content.parentElement;
        content.style.maxHeight = "100%";
      });
      ending_id[j]=i;
  }
  j++;

  let options = document.getElementsByClassName("letter");
  for (let i = ending_id[j]+1 ; i < options.length;i++){
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
updateLisners();

quizzes_list.addEventListener('scroll',function(){checkForExtraContent(quizzes_list,".add-quiz");});
question_list.addEventListener('scroll',function(){checkForExtraContent(question_list,".add-question");});


let id=-1;
let showPrompt2 =  (function(){
  
  let promptEl = document.querySelector('.prompt2'),_cb = null;
  
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


let add_quiz = document.querySelector(".add-quiz");
add_quiz.addEventListener('click',function(){
  let quiz_name = "";
  showPrompt('You need to provide your quiz name to continue!', function( answer ){
    quiz_name = answer;
    if (quiz_name!=""){
      createNewQuiz(quiz_name);
    }
  });  
})

document.querySelector(".prompt__cancel").addEventListener('click',function(){
  document.querySelector('.prompt').classList.remove('prompt--show');
});
document.querySelector(".prompt__cancel2").addEventListener('click',function(){
  document.querySelector('.prompt2').classList.remove('prompt2--show');
});

let add_question = document.querySelector(".add-question");
add_question.addEventListener('click',function(){
  showPrompt2('You need to provide information about the question to continue!', function(question_name,option_1,option_2,option_3,option_4){
    if (question_name!=""){
      createNewQuestion(question_name,option_1,option_2,option_3,option_4);
    }
  });  
});

function createNewQuiz(quiz_name) {
  fetch('/workspace', {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify({
      'quiz_name': quiz_name,
    })
  })
      .then(function (response) {

        if (response.ok) {
          response.json()
              .then(function (response) {
                console.log(response);
              });
        } else {
          throw Error('Something went wrong');
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  let node = createSection("div", "previous-quiz quiz-1");
  let child1 = document.createElement("div");
  let child2 = document.createElement("a");
  child2.href = "#";




  child2.appendChild(document.createTextNode(quiz_name));
  child1.appendChild(child2);
  node.appendChild(child1);
  child1 = createSection("div", "icons-container");
  child2 = createSection("label", "switch");
  let child3 = document.createElement("input");
  let child4 = createSection("span", "slider");
  child3.type = "checkbox";
  child2.append(child3, child4);
  child1.append(child2);
  child3 = createSection("button", "delete-quiz icon");
  child4 = createSection("i", "fa fa-trash");
  child3.appendChild(child4);
  child1.append(child3);
  node.append(child1);
  let quizzes = document.querySelector(".quizzes-list");
  quizzes.insertBefore(node, add_quiz);
  updateLisners();
}

function createNewQuestion(questoin_statement, option_1,option_2,option_3,option_4){
  
  let node = createSection("div","question_1");
  let panel = createSection("div","question-panel flex-center");
  let child1 = createSection("div","question-statement");
  child1.contentEditable = "true";
  child1.appendChild(document.createTextNode(questoin_statement));
  panel.appendChild(child1);
  child1 = createSection("button","icon delete-question");
  let child2 = createSection("i","fa fa-trash");
  child1.appendChild(child2);
  panel.appendChild(child1);
  child1 = createSection("button","icon expand-icon collapsible");
  child2 = createSection("i","fa fa-angle-down");
  child1.appendChild(child2);
  panel.appendChild(child1);
  node.appendChild(panel);
  panel = createSection("div","options-container");

  let options = [option_1,option_2,option_3,option_4];
  let chars = ["A","B","C","D"];
  for (let i=0;i<options.length;i++){
    child1 = createOption(chars[i],(id==i),options[i]);
    panel.appendChild(child1);
  }
  
  node.appendChild(panel);
  let questions_list = document.querySelector(".questions-list");
  let add_question = document.querySelector(".add-question");
  questions_list.insertBefore(node,add_question);
  updateLisners();
}

