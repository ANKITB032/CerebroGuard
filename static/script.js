document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('email-form');
    const resultsContainer = document.getElementById('results-container');
    const resultsDiv = document.getElementById('results');
    const analyzeBtn = document.getElementById('analyze-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        // Show loading state
        analyzeBtn.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;

        const sender = document.getElementById('sender').value;
        const recipient = document.getElementById('recipient').value;
        const body = document.getElementById('body').value;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
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
            // Restore button state
            analyzeBtn.textContent = 'Analyze Email';
            analyzeBtn.disabled = false;
        }
    });

    function displayResults(data) {
        resultsDiv.innerHTML = ''; // Clear previous results
        
        const score = data.risk_score;
        let scoreClass = 'score-low';
        if (score >= 40 && score < 70) {
            scoreClass = 'score-medium';
        } else if (score >= 70) {
            scoreClass = 'score-high';
        }

        const scoreElement = document.createElement('div');
        scoreElement.className = `score ${scoreClass}`;
        scoreElement.textContent = `${score}%`;
        
        const scoreTitle = document.createElement('h3');
        scoreTitle.textContent = 'Overall Risk Score';

        resultsDiv.appendChild(scoreTitle);
        resultsDiv.appendChild(scoreElement);

        const evidenceList = document.createElement('ul');
        data.evidence_factors.forEach(factor => {
            const item = document.createElement('li');
            const factorClass = factor.risk_contribution > 0 ? 'factor-negative' : 'factor-positive';
            item.className = factorClass;

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