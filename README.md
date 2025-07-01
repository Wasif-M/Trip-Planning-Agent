# Multi-Agent Trip Planner

## Overview
Multi-Agent Trip Planner is an AI-powered travel assistant that crafts personalized travel plans using a team of specialized agents. Each agent focuses on a unique aspect of your journey, working together to deliver a seamless, real-time, and budget-friendly travel experience.

---

## Features
- **Real-Time Destination Search:** Gathers up-to-date information about your chosen location, including top sights and local culture.
- **Live Weather Updates:** Integrates current weather forecasts for your destination to help you plan each day.
- **Local Advice:** Provides insider tips, hidden gems, and authentic experiences from a local perspective.
- **Event-Based Itinerary:** Divides your trip into distinct events and activities, creating a day-by-day schedule.
- **Budget Planning:** Estimates costs for every aspect of your trip, helping you manage your budget.
- **Comprehensive Travel Report:** Compiles all findings into a clear, easy-to-follow travel report.

---

## Agent Flow
1. **Destination Data Researcher:** Performs real-time web search to gather essential information about your destination.
2. **Weather Updater:** Fetches the latest weather forecasts for your travel dates.
3. **Local Expert:** Offers local advice, hidden gems, and unique experiences.
4. **Itinerary Planner:** Organizes your trip into daily events and activities.
5. **Budget Advisor:** Calculates estimated costs for each event and the overall trip.
6. **Travel Summary:** Compiles all data into a personalized travel report.

**Flow:**
```
Destination & Days → Real-Time Search & Weather → Local Advice → Event-Based Itinerary → Budget Plan → Personalized Trip Report
```

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Wasif-M/Trip-Planning-Agent.git
   cd Trip-Planning-Agent/mytripplanner
   ```
2. **Install dependencies:**
   ```bash
   pip install -r web/requirements.txt
   ```
3. **Run the application:**
   ```bash
   cd web
   python app.py
   ```
4. **Open your browser and visit:**
   [http://localhost:5000](http://localhost:5000)

---

## Usage
- Enter your destination and number of days on the home page.
- The system will show real-time progress as each agent completes its task.
- Once finished, you'll receive a detailed, event-based itinerary and budget report.

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements, bug fixes, or new features.

---

