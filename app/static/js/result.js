document.addEventListener('DOMContentLoaded', function() {
    const requestId = new URLSearchParams(window.location.search).get('request_id');
    const loadingContainer = document.getElementById('loading-container');
    const resultContent = document.getElementById('result-content');
    const resultText = document.getElementById('result-text');
    const tooltip = document.getElementById('tooltip');

    function formatCurrency(num) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(num);
    }

    function formatPercentage(num) {
        return new Intl.NumberFormat('en-US', {
            style: 'percent',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(num / 100);
    }

    function formatTime(days) {
        if (days >= 365) {
            return (days / 365).toFixed(2) + ' years';
        } else if (days >= 30) {
            return (days / 30).toFixed(2) + ' months';
        } else {
            return days + ' days';
        }
    }

    function formatRatio(num) {
        return num.toFixed(2);
    }

    function checkResult() {
        fetch(`/check_result?request_id=${requestId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'pending') {
                setTimeout(checkResult, 1000);
            } else {
                loadingContainer.style.display = 'none';
                resultContent.style.display = 'block';
                
                resultText.innerHTML = `Overall Profit: <span>${formatCurrency(data.profit)}</span> in <span>${formatTime(data.days_invested)}</span>`;

                document.getElementById('total-investment').textContent = formatCurrency(data.total_investment);
                document.getElementById('starting-principal').textContent = formatCurrency(data.starting_principal);
                document.getElementById('total-contributions').textContent = formatCurrency(data.total_contributions);
                document.getElementById('final-value').textContent = formatCurrency(data.final_value);

                document.getElementById('profit-percentage-overall').textContent = formatPercentage(data.profit_percentage_overall);
                document.getElementById('profit-percentage-per-year').textContent = formatPercentage(data.profit_percentage_per_year);
                document.getElementById('best-year-return').textContent = formatPercentage(data.best_year_return);
                document.getElementById('worst-year-return').textContent = formatPercentage(data.worst_year_return);

                document.getElementById('volatility').textContent = formatPercentage(data.volatility);
                document.getElementById('max-drawdown').textContent = formatPercentage(data.max_drawdown);
                document.getElementById('sharpe-ratio').textContent = formatRatio(data.sharpe_ratio);
                document.getElementById('sortino-ratio').textContent = formatRatio(data.sortino_ratio);

                setupTooltips();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function setupTooltips() {
        const tooltipElements = document.querySelectorAll('.tooltip');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', showTooltip);
            element.addEventListener('mouseleave', hideTooltip);
            element.addEventListener('touchstart', showTooltip, {passive: true});
            element.addEventListener('touchend', hideTooltip);
        });
    }

    function showTooltip(event) {
        const tooltipText = this.getAttribute('data-tooltip');
        tooltip.textContent = tooltipText;
        tooltip.style.opacity = '1';
        
        const rect = this.getBoundingClientRect();
        tooltip.style.left = `${rect.left + window.scrollX}px`;
        tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
    }

    function hideTooltip() {
        tooltip.style.opacity = '0';
    }

    checkResult();
});