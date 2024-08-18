document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('investment-form');
    const submitButton = document.getElementById('submit-button');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const dateError = document.getElementById('date-error');
    const startDateError = document.getElementById('start-date-error');
    const startingPrincipalInput = document.getElementById('starting-principal');
    const autoInvestAmountInput = document.getElementById('auto-invest-amount');
    const startingPrincipalError = document.getElementById('starting-principal-error');
    const autoInvestAmountError = document.getElementById('auto-invest-amount-error');
    const frequencySelect = document.getElementById('frequency');
    const intervalGroup = document.getElementById('interval-group');
    const investmentIntervalSelect = document.getElementById('investment-interval');

    const requiredInputs = [
        document.getElementById('etf-symbol'),
        startDateInput,
        endDateInput,
        startingPrincipalInput,
        autoInvestAmountInput,
        frequencySelect
    ];

    function checkFormValidity() {
        let isValid = true;

        requiredInputs.forEach(input => {
            const errorMessage = input.nextElementSibling;
            if (!input.value) {
                isValid = false;
                if (input.classList.contains('touched')) {
                    errorMessage.textContent = 'This field is required.';
                    input.classList.add('invalid');
                }
            } else {
                errorMessage.textContent = '';
                input.classList.remove('invalid');
            }
        });

        // Validate date range
        const startDate = new Date(startDateInput.value);
        const endDate = new Date(endDateInput.value);
        if (startDate >= endDate) {
            dateError.textContent = 'End date must be later than start date.';
            startDateInput.classList.add('invalid');
            endDateInput.classList.add('invalid');
            isValid = false;
        } else {
            dateError.textContent = '';
            startDateInput.classList.remove('invalid');
            endDateInput.classList.remove('invalid');
        }

        // Special handling for investment interval
        if ((frequencySelect.value === 'weekly' || frequencySelect.value === 'bi-weekly')) {
            if (!investmentIntervalSelect.value) {
                isValid = false;
                if (investmentIntervalSelect.classList.contains('touched')) {
                    investmentIntervalSelect.classList.add('invalid');
                    investmentIntervalSelect.nextElementSibling.textContent = 'This field is required.';
                }
            } else {
                investmentIntervalSelect.classList.remove('invalid');
                investmentIntervalSelect.nextElementSibling.textContent = '';
            }
        }

        submitButton.disabled = !isValid;
    }

    function handleInput(event) {
        const inputElement = event.target;
        inputElement.classList.add('touched');
        checkFormValidity();
    }

    function handleFrequencyChange(event) {
        const frequency = event.target.value;
        if (frequency === 'weekly' || frequency === 'bi-weekly') {
            intervalGroup.classList.remove('hidden');
            investmentIntervalSelect.required = true;
        } else {
            intervalGroup.classList.add('hidden');
            investmentIntervalSelect.required = false;
            investmentIntervalSelect.value = '';
        }
        checkFormValidity();
    }

    form.addEventListener('input', handleInput);
    frequencySelect.addEventListener('change', handleFrequencyChange);

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Disable the submit button immediately after click
        submitButton.disabled = true;
        submitButton.textContent = 'Loading...';

        const formData = new FormData(event.target);
        const formObject = Object.fromEntries(formData.entries());

        fetch('/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formObject)
        })
        .then(response => response.json())
        .then(data => {
            const url = new URL(window.location.href);
            url.pathname = '/result';
            url.searchParams.set('request_id', data.request_id);
            window.location.href = url.toString();
        })
        .catch(error => {
            console.error('Error:', error);
            // Re-enable the button if there's an error
            submitButton.disabled = false;
            submitButton.textContent = 'Simulate Returns'; // Reset button text
        });
    });
});