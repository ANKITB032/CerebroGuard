document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('email-form');
  const resultsContainer = document.getElementById('results-container');
  const resultsDiv = document.getElementById('results');
  const analyzeBtn = document.getElementById('analyze-btn');
  const spinner = document.getElementById("loading-spinner");

  function validateEmailField(field) {
    const value = field.value.trim();
    const regex = /^[^@]+@[^@]+\.[^@]+$/;
    if (regex.test(value)) {
      field.classList.add("valid");
      field.classList.remove("invalid");
    } else {
      field.classList.add("invalid");
      field.classList.remove("valid");
    }
  }
  document.getElementById('sender').addEventListener('input', function() { validateEmailField(this); });
  document.getElementById('recipient').addEventListener('input', function() { validateEmailField(this); });

  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default form submission
    analyzeBtn.textContent = 'Analyzing...';
    analyzeBtn.disabled = true;
    spinner.classList.remove("hidden");

    const sender = document.getElementById('sender').value;
    const recipient = document.getElementById('recipient').value;
    const body = document.getElementById('body').value;
    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender, recipient, body }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      displayResults(data);
    } catch (error) {
      console.error('Error:', error);
      resultsDiv.innerHTML = `<p class="error">An error occurred. Please check the console for details.</p>`;
      resultsContainer.classList.remove('hidden');
    } finally {
      analyzeBtn.textContent = 'Analyze Email';
      analyzeBtn.disabled = false;
      spinner.classList.add("hidden");
    }
  });

  function animateScore(element, targetScore) {
    let current = 0;
    const step = targetScore > 50 ? 2 : 1;
    const interval = setInterval(function() {
      current += step;
      if(current >= targetScore) {
        current = targetScore;
        clearInterval(interval);
      }
      element.textContent = current + "%";
    }, 15); // smoother and faster

    // Also set the final color based on score
    let scoreClass = 'score-low';
    if (targetScore >= 40 && targetScore < 70) { scoreClass = 'score-medium'; }
    else if (targetScore >= 70) { scoreClass = 'score-high'; }
    element.className = `score ${scoreClass} results-animated`;
  }

  function displayResults(data) {
    resultsDiv.innerHTML = '';
    const score = data.risk_score || 0;
    const scoreElement = document.createElement('div');
    animateScore(scoreElement, score);

    const scoreTitle = document.createElement('h3');
    scoreTitle.textContent = 'Overall Risk Score';

    resultsDiv.appendChild(scoreTitle);
    resultsDiv.appendChild(scoreElement);

    const evidenceList = document.createElement('ul');
    (data.evidence_factors || []).forEach((factor, i) => {
      const item = document.createElement('li');
      const factorClass = factor.risk_contribution > 0 ? 'factor-negative' : 'factor-positive';
      item.className = `${factorClass} results-animated`;
      setTimeout(() => { item.classList.add("results-animated"); }, 50 * i);

      const finding = document.createElement('div');
      finding.className = 'factor-finding';
      finding.textContent = factor.finding;
      const details = document.createElement('div');
      details.className = 'factor-details';
      details.textContent = factor.details;

      item.appendChild(finding);
      item.appendChild(details);
      evidenceList.appendChild(item);
    });

    resultsDiv.appendChild(evidenceList);
    resultsContainer.classList.remove('hidden');
  }
});
