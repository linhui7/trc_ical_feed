# TRC iCal Feed

This project automatically fetches event calendars from four Triangle Rock Club locations, filters for selected event types, adds a location prefix to each event, and publishes a merged `.ics` file you can subscribe to in your iOS/macOS calendar.

## Features
- Fetches iCal feeds from:
  - TRC Durham  
  - TRC Morrisville  
  - TRC Raleigh  
  - TRC Salvage Yard  
- Keeps only:
  - **Member Guest Hours**
  - **Climbing Connections**
- Adds location prefixes to event titles  
  e.g., `TRC Durham - Member Guest Hours`
- Merges all events into one calendar file: `trc_filtered.ics`
- GitHub Actions runs automatically (daily + on push) to update the file
