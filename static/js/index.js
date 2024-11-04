// static/js/index.js
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('investment-form');
    const submitButton = document.getElementById('submit-button');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const dateError = document.getElementById('date-error');
    const startingPrincipalInput = document.getElementById('starting-principal');
    const autoInvestAmountInput = document.getElementById('auto-invest-amount');
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

    // Initialize form validation state
    let formValid = false;

    // Function to check form validity
    function checkFormValidity() {
        let isValid = true;

        // Reset all error messages
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
        if (frequencySelect.value === 'weekly' || frequencySelect.value === 'bi-weekly') {
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

    // Handle input events
    function handleInput(event) {
        const inputElement = event.target;
        inputElement.classList.add('touched');
        checkFormValidity();
    }

    // Handle frequency change to show/hide investment interval
    function handleFrequencyChange(event) {
        const frequency = event.target.value;
        if (frequency === 'weekly' || frequency === 'bi-weekly') {
            intervalGroup.classList.remove('hidden');
            investmentIntervalSelect.required = true;
        } else {
            intervalGroup.classList.add('hidden');
            investmentIntervalSelect.required = false;
            investmentIntervalSelect.value = '';
            investmentIntervalSelect.classList.remove('invalid');
            investmentIntervalSelect.nextElementSibling.textContent = '';
        }
        checkFormValidity();
    }

    // Attach event listeners to form inputs
    requiredInputs.forEach(input => {
        input.addEventListener('input', handleInput);
    });
    frequencySelect.addEventListener('change', handleFrequencyChange);
    investmentIntervalSelect.addEventListener('input', handleInput);

    // Handle form submission
    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent default form submission

        // Collect form data
        const formData = {
            etf_symbol: document.getElementById('etf-symbol').value,
            start_date: startDateInput.value,
            end_date: endDateInput.value,
            starting_principal: parseFloat(startingPrincipalInput.value),
            auto_invest_amount: parseFloat(autoInvestAmountInput.value),
            investment_interval: investmentIntervalSelect.value || '',
            frequency: frequencySelect.value
        };

        // Disable the submit button to prevent multiple submissions
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';

        try {
            // Send data to /simulate endpoint
            const simulateResponse = await fetch('/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const simulateResult = await simulateResponse.json();

            if (!simulateResponse.ok) {
                // Handle errors from /simulate
                alert(`Error: ${simulateResult.error}`);
                submitButton.disabled = false;
                submitButton.textContent = 'Simulate Returns';
                return;
            }

            // Send base parameters to /set_base endpoint
            const setBaseResponse = await fetch('/set_base', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ new_base_params: formData })
            });

            const setBaseResult = await setBaseResponse.json();

            if (!setBaseResponse.ok) {
                // Handle errors from /set_base
                alert(`Error: ${setBaseResult.error}`);
                submitButton.disabled = false;
                submitButton.textContent = 'Simulate Returns';
                return;
            }

            // Redirect to compare.html
            window.location.href = '/compare';

        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again.');
            submitButton.disabled = false;
            submitButton.textContent = 'Simulate Returns';
        }
    });
});