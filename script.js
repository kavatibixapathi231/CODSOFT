let quizzes = [];
  {
    id: 'general-knowledge',
    title: 'General Knowledge',
    category: 'General',
    questions: [
      {
        text: 'Which planet is known as the Red Planet?',
        choices: ['Earth', 'Mars', 'Jupiter', 'Venus'],
        answer: 1,
        explanation: 'Mars is nicknamed the Red Planet due to its reddish appearance.',
      },
      {
        text: 'What is the fastest land animal?',
        choices: ['Cheetah', 'Lion', 'Horse', 'Greyhound'],
        answer: 0,
        explanation: 'The cheetah can reach speeds up to 75 mph in short bursts.',
      },
      {
        text: 'Which element has the chemical symbol O?',
        choices: ['Gold', 'Oxygen', 'Osmium', 'Silver'],
        answer: 1,
        explanation: 'Oxygen is represented by the symbol O.',
      },
    ],
  },
  {
    id: 'space-exploration',
    title: 'Space Exploration',
    category: 'Science',
    questions: [
      {
        text: 'Which moon orbits the planet Saturn and is famous for its icy surface?',
        choices: ['Europa', 'Titan', 'Io', 'Ganymede'],
        answer: 1,
        explanation: 'Titan is Saturn’s largest moon and has a thick atmosphere.',
      },
      {
        text: 'What is the name of the first artificial satellite launched by humans?',
        choices: ['Voyager 1', 'Sputnik 1', 'Apollo 11', 'Hubble'],
        answer: 1,
        explanation: 'Sputnik 1 was launched by the Soviet Union in 1957.',
      },
      {
        text: 'Which planet has a prominent ring system?',
        choices: ['Mars', 'Venus', 'Saturn', 'Mercury'],
        answer: 2,
        explanation: 'Saturn is famous for its visible rings.',
      },
    ],
  },
  {
    id: 'history',
    title: 'World History',
    category: 'History',
    questions: [
      {
        text: 'Which ancient civilization built the pyramids at Giza?',
        choices: ['Romans', 'Greeks', 'Egyptians', 'Mayans'],
        answer: 2,
        explanation: 'The pyramids at Giza were built by ancient Egyptians.',
      },
      {
        text: 'Who was the first president of the United States?',
        choices: ['Thomas Jefferson', 'George Washington', 'John Adams', 'Abraham Lincoln'],
        answer: 1,
        explanation: 'George Washington served as the first U.S. president.',
      },
      {
        text: 'What year did the Berlin Wall fall?',
        choices: ['1981', '1989', '1993', '1978'],
        answer: 1,
        explanation: 'The Berlin Wall fell in 1989, marking the end of an era.',
      },
    ],
  },
];

const homeScreen = document.getElementById('homeScreen');
const quizScreen = document.getElementById('quizScreen');
const resultScreen = document.getElementById('resultScreen');
const quizList = document.getElementById('quizList');
const randomQuizButton = document.getElementById('randomQuizButton');
const homeButton = document.getElementById('homeButton');
const submitButton = document.getElementById('submitButton');
const nextButton = document.getElementById('nextButton');
const restartButton = document.getElementById('restartButton');
const quizTitle = document.getElementById('quizTitle');
const quizCategory = document.getElementById('quizCategory');
const currentScore = document.getElementById('currentScore');
const questionIndexLabel = document.getElementById('questionIndex');
const currentQuestionNumber = document.getElementById('currentQuestionNumber');
const totalQuestions = document.getElementById('totalQuestions');
const questionText = document.getElementById('questionText');
const optionsForm = document.getElementById('optionsForm');
const feedbackMessage = document.getElementById('feedbackMessage');
const finalScore = document.getElementById('finalScore');
const finalTotal = document.getElementById('finalTotal');
const resultDetails = document.getElementById('resultDetails');

let activeQuiz = null;
let activeIndex = 0;
let score = 0;
let selectedOption = null;
let answers = [];

function showScreen(screen) {
  homeScreen.classList.remove('active');
  quizScreen.classList.remove('active');
  resultScreen.classList.remove('active');
  screen.classList.add('active');
}

function renderQuizList() {
  quizList.innerHTML = '';
  quizzes.forEach((quiz) => {
    const card = document.createElement('div');
    card.className = 'quiz-item';
    card.innerHTML = `
      <h4>${quiz.title}</h4>
      <p>${quiz.questions.length} questions</p>
      <button class="secondary-button" data-quiz="${quiz.id}">Start Quiz</button>
    `;
    quizList.appendChild(card);
  });
}

function resetState() {
  activeIndex = 0;
  score = 0;
  selectedOption = null;
  answers = [];
  feedbackMessage.className = 'feedback-box hidden';
  submitButton.disabled = true;
  nextButton.classList.add('hidden');
}

function openQuiz(quizId) {
  const quiz = quizzes.find((item) => item.id === quizId);
  if (!quiz) return;
  activeQuiz = quiz;
  resetState();
  quizTitle.textContent = quiz.title;
  quizCategory.textContent = quiz.category;
  currentScore.textContent = score;
  totalQuestions.textContent = quiz.questions.length;
  questionIndexLabel.textContent = `${activeIndex}/${quiz.questions.length}`;
  homeButton.classList.remove('hidden');
  renderQuestion();
  showScreen(quizScreen);
}

function renderQuestion() {
  const question = activeQuiz.questions[activeIndex];
  currentQuestionNumber.textContent = activeIndex + 1;
  questionText.textContent = question.text;
  optionsForm.innerHTML = '';
  selectedOption = null;
  submitButton.disabled = true;
  nextButton.classList.add('hidden');
  feedbackMessage.className = 'feedback-box hidden';

  question.choices.forEach((choice, index) => {
    const optionCard = document.createElement('label');
    optionCard.className = 'option-card';
    optionCard.innerHTML = `
      <input type="radio" name="option" value="${index}" />
      <span>${choice}</span>
    `;

    const input = optionCard.querySelector('input');
    input.addEventListener('change', () => {
      selectedOption = Number(input.value);
      submitButton.disabled = false;
      document.querySelectorAll('.option-card').forEach((card) => card.classList.remove('selected'));
      optionCard.classList.add('selected');
    });

    optionsForm.appendChild(optionCard);
  });
}

function showFeedback(isCorrect, explanation) {
  feedbackMessage.className = `feedback-box ${isCorrect ? 'success' : 'error'}`;
  feedbackMessage.textContent = isCorrect
    ? `Correct! ${explanation}`
    : `Incorrect. ${explanation}`;
}

function submitAnswer() {
  if (selectedOption === null) return;
  const question = activeQuiz.questions[activeIndex];
  const isCorrect = selectedOption === question.answer;
  if (isCorrect) score += 1;
  answers.push({
    question: question.text,
    selected: question.choices[selectedOption],
    correct: question.choices[question.answer],
    isCorrect,
    explanation: question.explanation,
  });
  currentScore.textContent = score;
  questionIndexLabel.textContent = `${activeIndex + 1}/${activeQuiz.questions.length}`;
  submitButton.disabled = true;
  nextButton.classList.remove('hidden');
  showFeedback(isCorrect, question.explanation);
}

function moveToNextQuestion() {
  activeIndex += 1;
  if (activeIndex >= activeQuiz.questions.length) {
    showResults();
    return;
  }
  questionIndexLabel.textContent = `${activeIndex}/${activeQuiz.questions.length}`;
  renderQuestion();
}

function showResults() {
  finalScore.textContent = score;
  finalTotal.textContent = activeQuiz.questions.length;
  resultDetails.innerHTML = '';

  answers.forEach((answer, index) => {
    const item = document.createElement('div');
    item.className = 'result-item';
    item.innerHTML = `
      <strong>Question ${index + 1}</strong>
      <p>${answer.question}</p>
      <p>Selected: ${answer.selected}</p>
      <p>Correct: ${answer.correct}</p>
      <p class="hint">${answer.isCorrect ? 'Nice work!': 'Review this explanation:'} ${answer.explanation}</p>
    `;
    resultDetails.appendChild(item);
  });

  showScreen(resultScreen);
}

function returnHome() {
  activeQuiz = null;
  homeButton.classList.add('hidden');
  showScreen(homeScreen);
}

randomQuizButton.addEventListener('click', () => {
  const randomQuiz = quizzes[Math.floor(Math.random() * quizzes.length)];
  openQuiz(randomQuiz.id);
});

homeButton.addEventListener('click', returnHome);
restartButton.addEventListener('click', returnHome);
submitButton.addEventListener('click', (event) => {
  event.preventDefault();
  submitAnswer();
});
nextButton.addEventListener('click', moveToNextQuestion);

quizList.addEventListener('click', (event) => {
  const button = event.target.closest('button');
  if (!button) return;
  const quizId = button.dataset.quiz;
  if (quizId) openQuiz(quizId);
});

renderQuizList();
showScreen(homeScreen);
