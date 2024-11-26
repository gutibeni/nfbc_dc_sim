#  Fantasy Baseball Auction Draft Simulation

## Overview
This project simulates a NFBC Draft Champions fantasy baseball season (15-team league) using Monte Carlo methods. 
It evaluates team performance based on the roto scoring system. The purpose of the simulation is 
use custom preseason category weights to experiment with draft strategies.

## Features
* Custom Weighting: Simulate strategies with user-defined weights for statistical categories.
* Snake Draft Simulation: Draft players using a 15-team snake draft format.
* Weekly Lineup Management: Generate weekly lineups optimized for scoring.
* Roto Scoring System: Teams score points based on rankings in each category.
* Season Metrics: Analyze results with metrics like average position, percent first-place finishes, and more.

## Roto Scoring
* Standard Categories: Higher totals score better (e.g., HR, RBI, etc.).
* Rate Stats: For ERA and WHIP, lower values score better.

## Requirements
* Python 3.8 or higher
* Required libraries:
  * pandas
  * numpy
  * scikit-learn

## Installation
  1. Clone the repository:
  `bash
  git clone https://github.com/yourusername/fantasy-baseball-sim.git
cd fantasy-baseball-sim`


  2. Install dependencies:
  `bash
  Copy code
  pip install -r requirements.txt`
  
## Usage
1. Prepare data files:
    * Steamer projections in CSV format for hitters and pitchers.
    * Example:
      * hitters_steamer_2024.csv
      * pitchers_steamer_2024.csv

2. Run the simulation:
`
bash
python fantasy_baseball_simulation.py`

3. Customize weights: Modify the weights_list variable in the script to experiment with strategies.

4. Example output:
   * Average position of the test team.
   * Percent of simulations where the test team finishes first.
   * Full roto standings for all teams.

## Project Structure
`
├── fantasy_baseball_simulation.py  # Main simulation script
├── test_fantasy_baseball_simulation.py  # Unit tests
├── hitters_steamer_2024.csv  # Sample data (replace with real data)
├── pitchers_steamer_2024.csv  # Sample data (replace with real data)
└── README.md  # Project documentation`

# Testing
Run unit tests with:

`bash
Copy code
python -m unittest test_fantasy_baseball_simulation.py`

## Future Enhancements
* Incorporate ADP
* Use other projection models beyond steamer
* Utilize other historical seasons (Currently using 2024 preseason projections)
* Summarize player performance for the simulated seasons (e.g., average stat lines for the highest performing players by position and/or category)
* Support for auction drafts.
* Other league types (Add support for dynamic roster changes during the season).
* Enhanced visualizations for standings and performance metrics.

## License
MIT License.

Contact
For questions or contributions, contact @gutibeni or open an issue on GitHub.
