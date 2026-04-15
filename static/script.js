const prompts = [
    "What genre are you looking for?",
    "What length book are you looking for? (novella, standard novel, epic)",
    "Test this one"
];

const labels = [
    "Genre:",
    "Length:",
    "ok"
];

let currentQuestion = 0;
let responses = [];

const promptElement = document.getElementById('prompt');
const inputElement = document.getElementById('userInput');
const submitBtn = document.getElementById('submitBtn');
const responseList = document.getElementById('responseList');

function updatePrompt() {
    if (currentQuestion < prompts.length) {
        promptElement.textContent = prompts[currentQuestion];
        inputElement.value = '';
        inputElement.focus();
    }
}

function displayResponse(label, answer) {
    const responseItem = document.createElement('div');
    responseItem.className = 'response-item';
    responseItem.innerHTML = `<strong>${label}</strong><span>${answer}</span>`;
    responseList.appendChild(responseItem);
}

function handleSubmit() {
    const userAnswer = inputElement.value.trim();
    
    if (userAnswer === '') {
        return;
    }
    
    responses.push(userAnswer);
    console.log(responses);
    displayResponse(labels[currentQuestion], userAnswer);
    
    currentQuestion++;
    
    if (currentQuestion < prompts.length) {
        updatePrompt();
    } else {
        promptElement.textContent = "Thank you! Your preferences have been recorded.";
        inputElement.style.display = 'none';
        submitBtn.style.display = 'none';
    }
}

submitBtn.addEventListener('click', handleSubmit);

inputElement.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSubmit();
    }
});

// Initialize first question
updatePrompt();