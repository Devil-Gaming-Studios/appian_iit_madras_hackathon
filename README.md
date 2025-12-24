Predictive Operations Simulation Dashboard

This project is a predictive operations dashboard that simulates SLA-driven business processes.
It enables proactive forecasting, what-if scenario analysis, and AI-assisted staffing optimization using live operational inputs.

Features

SLA breach probability prediction using simulation

Backlog forecasting based on current work in progress

What-if scenario testing (staffing and automation changes)

AI-based staffing optimizer with feasibility analysis

Interactive web-based UI

Tech Stack

Python 3

Streamlit

NumPy

Pandas

Project Structure
app.py            # Main Streamlit application
simulation.py     # Predictive simulation logic
scenario.py       # What-if scenario calculations
requirements.txt  # Python dependencies

How to Run
1. Install Python

Ensure Python 3.8 or above is installed.

Check:

python --version

2. Install Dependencies
python -m pip install -r requirements.txt

3. Run the Application
python -m streamlit run app.py


The application will be available at:

http://localhost:8501

Usage

Adjust operational inputs from the sidebar

View SLA risk and backlog forecast

Test scenarios in the simulation tab

Use the AI optimizer to identify optimal staffing levels

Purpose

This project demonstrates how predictive simulation and decision intelligence can be applied to SLA-critical operational workflows.
