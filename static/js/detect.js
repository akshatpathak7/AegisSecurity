document.addEventListener('DOMContentLoaded', function () {
    // Tab switching
    document.querySelectorAll('.detect-tab').forEach(function (tab) {
        tab.addEventListener('click', function () {
            document.querySelectorAll('.detect-tab').forEach(function (t) { t.classList.remove('active'); });
            document.querySelectorAll('.detect-panel').forEach(function (p) { p.classList.remove('active'); });
            this.classList.add('active');
            document.getElementById('panel-' + this.dataset.tab).classList.add('active');
            hideResult();
        });
    });

    // File upload zones
    document.getElementById('emailUpload').addEventListener('click', function () {
        document.getElementById('emailFile').click();
    });

    document.getElementById('voiceUpload').addEventListener('click', function () {
        document.getElementById('voiceFile').click();
    });

    document.getElementById('emailFile').addEventListener('change', function () {
        document.getElementById('emailFileName').textContent = this.files[0] ? this.files[0].name : '';
    });

    document.getElementById('voiceFile').addEventListener('change', function () {
        document.getElementById('voiceFileName').textContent = this.files[0] ? this.files[0].name : '';
    });
});

/* Helpers */
function showLoading() {
    document.getElementById('loading').classList.add('show');
    hideResult();
}

function hideLoading() {
    document.getElementById('loading').classList.remove('show');
}

function hideResult() {
    document.getElementById('resultBox').classList.remove('show');
}

function escapeHtml(text) {
    var d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
}

/* Render result into the new structure */
function showResult(data) {
    hideLoading();
    var container = document.getElementById('resultBox');
    var panel = document.getElementById('resultPanel');
    var icon = document.getElementById('resultIcon');
    var title = document.getElementById('resultTitle');
    var meta = document.getElementById('resultMeta');
    var meter = document.getElementById('confidenceMeter');
    var confVal = document.getElementById('confidenceValue');
    var confFill = document.getElementById('confidenceFill');
    var transcript = document.getElementById('resultTranscript');
    var actions = document.getElementById('resultActions');

    panel.classList.remove('is-threat', 'is-safe', 'is-error');

    if (data.error) {
        panel.classList.add('is-error');
        icon.innerHTML = '<svg viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.4"/><path d="M7.5 7.5l5 5M12.5 7.5l-5 5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>';
        icon.style.background = 'var(--bg-elevated)';
        icon.style.color = 'var(--text-secondary)';
        title.textContent = 'Analysis error';
        title.style.color = 'var(--text-primary)';
        meta.textContent = data.error;
        meter.style.display = 'none';
        actions.innerHTML = '';
        transcript.style.display = 'none';
        container.classList.add('show');
        return;
    }

    meter.style.display = '';

    if (data.is_attack) {
        panel.classList.add('is-threat');
        icon.innerHTML = '<svg viewBox="0 0 20 20" fill="none"><path d="M10 2L2 17h16L10 2z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M10 8v4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><circle cx="10" cy="14" r="0.6" fill="currentColor"/></svg>';
        icon.style.background = '';
        icon.style.color = '';
        title.textContent = data.message;
        title.style.color = '';
        meta.textContent = 'Classification: ' + data.attack_label;
        actions.innerHTML =
            '<a href="/guidance/' + data.attack_type + '" class="btn btn-danger btn-sm">View guidance</a>' +
            '<a href="/library/' + data.attack_type + '" class="btn btn-secondary btn-sm">Learn about ' + data.attack_label + '</a>';
    } else {
        panel.classList.add('is-safe');
        icon.innerHTML = '<svg viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.4"/><path d="M7 10l2 2 4-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
        icon.style.background = '';
        icon.style.color = '';
        title.textContent = 'No threat detected';
        title.style.color = '';
        meta.textContent = 'This content appears safe';
        actions.innerHTML = '';
    }

    confVal.textContent = data.confidence + '%';
    confFill.style.width = data.confidence + '%';

    if (data.transcript) {
        transcript.style.display = 'block';
        transcript.innerHTML = '<strong>Transcript:</strong> ' + escapeHtml(data.transcript);
    } else {
        transcript.style.display = 'none';
    }

    container.classList.add('show');
}

/* API calls */
function analyzeText() {
    var text = document.getElementById('textInput').value.trim();
    if (!text) { showResult({ error: 'Enter some text to analyze.' }); return; }

    showLoading();
    fetch('/api/detect/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(function (r) { return r.json(); })
    .then(showResult)
    .catch(function () { showResult({ error: 'Analysis failed. Please try again.' }); });
}

function analyzeEmail() {
    var file = document.getElementById('emailFile').files[0];
    var pasted = document.getElementById('emailPaste').value.trim();

    if (file) {
        showLoading();
        var fd = new FormData();
        fd.append('file', file);
        fetch('/api/detect/email', { method: 'POST', body: fd })
            .then(function (r) { return r.json(); })
            .then(showResult)
            .catch(function () { showResult({ error: 'File analysis failed.' }); });
    } else if (pasted) {
        showLoading();
        fetch('/api/detect/email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: pasted })
        })
        .then(function (r) { return r.json(); })
        .then(showResult)
        .catch(function () { showResult({ error: 'Analysis failed.' }); });
    } else {
        showResult({ error: 'Paste email content or upload a file.' });
    }
}

function analyzeVoice() {
    var file = document.getElementById('voiceFile').files[0];
    if (!file) { showResult({ error: 'Upload an audio file first.' }); return; }

    showLoading();
    document.querySelector('.loader-text').textContent = 'Transcribing audio...';

    var fd = new FormData();
    fd.append('file', file);
    fetch('/api/detect/voice', { method: 'POST', body: fd })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            document.querySelector('.loader-text').textContent = 'Analyzing content...';
            showResult(data);
        })
        .catch(function () {
            document.querySelector('.loader-text').textContent = 'Analyzing content...';
            showResult({ error: 'Audio analysis failed. Whisper may not be installed.' });
        });
}
