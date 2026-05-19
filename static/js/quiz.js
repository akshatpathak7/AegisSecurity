var questions = [];
var currentIndex = 0;
var userAnswers = [];
var answered = false;

function startQuiz() {
    document.getElementById('quizStart').style.display = 'none';
    document.getElementById('quizResults').style.display = 'none';
    document.getElementById('quizArea').style.display = 'block';

    currentIndex = 0;
    userAnswers = [];
    answered = false;

    fetch('/api/quiz/questions')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            questions = data;
            renderQuestion();
        })
        .catch(function () {
            document.getElementById('questionText').textContent = 'Failed to load questions.';
        });
}

function renderQuestion() {
    if (currentIndex >= questions.length) { submitQuiz(); return; }

    answered = false;
    var q = questions[currentIndex];
    var pct = (currentIndex / questions.length) * 100;

    document.getElementById('progressFill').style.width = pct + '%';
    document.getElementById('progressText').textContent = (currentIndex + 1) + ' / ' + questions.length;
    document.getElementById('questionText').textContent = q.question;
    document.getElementById('nextBtn').style.display = 'none';
    document.getElementById('explanation').classList.remove('show');

    var opts = [
        { letter: 'A', text: q.option_a },
        { letter: 'B', text: q.option_b },
        { letter: 'C', text: q.option_c },
        { letter: 'D', text: q.option_d }
    ];

    var container = document.getElementById('optionsContainer');
    container.innerHTML = '';

    opts.forEach(function (opt) {
        var div = document.createElement('div');
        div.className = 'quiz-option';
        div.innerHTML =
            '<span class="option-letter">' + opt.letter + '</span>' +
            '<span class="option-text">' + opt.text + '</span>';
        div.addEventListener('click', function () { selectAnswer(opt.letter, div); });
        container.appendChild(div);
    });
}

function selectAnswer(letter) {
    if (answered) return;
    answered = true;

    var q = questions[currentIndex];
    var isCorrect = letter === q.correct_answer;

    userAnswers.push({ question_id: q.id, answer: letter });

    document.querySelectorAll('.quiz-option').forEach(function (el) {
        var l = el.querySelector('.option-letter').textContent;
        if (l === q.correct_answer) {
            el.classList.add('correct');
        } else if (l === letter && !isCorrect) {
            el.classList.add('incorrect');
        }
    });

    var exp = document.getElementById('explanation');
    exp.textContent = q.explanation;
    exp.classList.add('show');

    var btn = document.getElementById('nextBtn');
    btn.style.display = 'inline-flex';
    btn.innerHTML = currentIndex < questions.length - 1
        ? 'Next <svg viewBox="0 0 12 12" fill="none"><path d="M2.5 6h7M6.5 3l3 3-3 3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        : 'See results';
}

function nextQuestion() {
    currentIndex++;
    currentIndex >= questions.length ? submitQuiz() : renderQuestion();
}

function submitQuiz() {
    document.getElementById('quizArea').style.display = 'none';

    fetch('/api/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: userAnswers })
    })
    .then(function (r) { return r.json(); })
    .then(showResults)
    .catch(function () {
        document.getElementById('quizResults').style.display = 'block';
        document.getElementById('scoreMessage').textContent = 'Submission failed.';
    });
}

function showResults(data) {
    document.getElementById('quizResults').style.display = 'block';
    document.getElementById('scoreNumber').textContent = data.score + '%';
    document.getElementById('scoreDetail').textContent =
        data.correct + ' of ' + data.total + ' correct';

    var ring = document.getElementById('scoreCircle');
    var num = document.getElementById('scoreNumber');
    var msg = document.getElementById('scoreMessage');

    if (data.score >= 80) {
        ring.style.borderColor = 'var(--success)';
        num.style.color = 'var(--success)';
        msg.textContent = 'Strong awareness';
    } else if (data.score >= 50) {
        ring.style.borderColor = 'var(--warning)';
        num.style.color = 'var(--warning)';
        msg.textContent = 'Room for improvement';
    } else {
        ring.style.borderColor = 'var(--danger)';
        num.style.color = 'var(--danger)';
        msg.textContent = 'Review recommended';
    }

    var bd = document.getElementById('resultsBreakdown');
    bd.innerHTML = '<div class="breakdown-title">Breakdown</div>';

    data.results.forEach(function (r, i) {
        var q = questions[i];
        if (!q) return;

        var div = document.createElement('div');
        div.className = 'breakdown-item';

        var iconClass = r.correct ? 'is-correct' : 'is-wrong';
        var iconSvg = r.correct
            ? '<svg viewBox="0 0 12 12" fill="none"><path d="M3 6l2.5 2.5L9 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            : '<svg viewBox="0 0 12 12" fill="none"><path d="M4 4l4 4M8 4l-4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>';

        div.innerHTML =
            '<div class="breakdown-icon ' + iconClass + '">' + iconSvg + '</div>' +
            '<div>' +
                '<div class="breakdown-q">' + q.question + '</div>' +
                (r.correct ? '' : '<div class="breakdown-exp">Answer: ' + r.correct_answer + ' — ' + r.explanation + '</div>') +
            '</div>';

        bd.appendChild(div);
    });
}
