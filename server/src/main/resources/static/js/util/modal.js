const okModalBodyElement = document.querySelector('#ok-modal-body');
const questionModalBodyElement = document.querySelector('#question-modal-body');
const okModalBtnElement = document.querySelector("#ok-modal-btn");
const questionModalBtnElement = document.querySelector("#question-modal-btn");

function showOkModal(text, func = ()=>{}) {
    const okModal = new bootstrap.Modal('#ok-modal');
    okModalBodyElement.textContent = text;
    okModalBtnElement.onclick = func;
    okModal.show();
}

function showQuestionModal(text, func = ()=>{}){
    const questionModal = new bootstrap.Modal('#question-modal');
    questionModalBodyElement.textContent = text;
    questionModalBtnElement.onclick = func;
    questionModal.show();
}