# ETF Investment Simulator

A web application that allows users to simulate and compare different ETF investment strategies over time. Users can create multiple investment scenarios with different parameters and visualize their performance.

## Features

- Simulate ETF investments with customizable parameters
- Compare multiple investment scenarios side by side
- Interactive data visualization
- Responsive design for desktop and mobile devices
- Real-time form validation
- Customizable metrics display

## Project Structure

```
├── app.py               # Flask application entry point
├── invest.py            # Investment simulation logic and plotting
├── data.py              # Data fetching and storage
├── test.py              # Unit tests
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── static/
│   ├── css/
│   │   └── index.css    # Main stylesheet
│   └── js/
│       └── index.js     # Frontend JavaScript
├── templates/
│   ├── index.html       # Main investment form page
│   └── compare.html     # Investment comparison page
└── data/                # Data folder, populated by data.py
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd etf-investment-simulator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Testing

First, start the Flask server:
```bash
python app.py
```

Then, in a new terminal, run the test suite:
```bash
python -m unittest test.py
```

## Usage

1. **Main Simulation Page**
   - Enter ETF symbol
   - Set investment period
   - Define starting principal
   - Configure auto-investment amount
   - Choose investment frequency
   - Select specific days for weekly/bi-weekly investments

2. **Comparison Page**
   - View multiple investment scenarios
   - Compare key metrics
   - Visualize performance over time
   - Add/edit/delete investment sets
   - Customize displayed metrics

## API Endpoints

1. **/simulate** (POST)
   - Simulates investment strategy
   - Required parameters:
     - etf_symbol
     - start_date
     - end_date
     - starting_principal
     - auto_invest_amount
     - frequency
     - investment_interval (for weekly/bi-weekly)

2. **/set_base** (POST)
   - Sets base parameters for comparison in Flask session
   - Requires new_base_params object

3. **/get_base** (GET)
   - Retrieves current base parameters