# UFC Statistics Platform

## A full-stack UFC statistics platform that collects, stores, and queries data about UFC fighters, fights, and events.

**Overview**

This project is designed to provide an easy way to explore UFC data without needing to write SQL queries or manually scrape statistics websites. The platform uses Python web scraping scripts to gather data, stores the data in a MySQL database, and is being developed into a full-stack web application with a Spring Boot backend and React frontend.

The project is currently in active development.

⸻

Features

Current Features

* Python web scraping pipelines for UFC data collection
* MySQL relational database for fighter, fight, and event data
* Automated data insertion and database population
* Dockerized services
* Hosted on a personal Linux server

Planned Features

* React frontend for user-friendly data exploration
* Spring Boot REST API backend
* Advanced filtering and search capabilities
* Fighter comparison tools
* Event and matchup statistics pages
* Data visualization and analytics

⸻

Tech Stack

Backend

* Java
* Spring Boot

Frontend

* React
* TypeScript / JavaScript

Database

* MySQL

Data Collection

* Python
* Selenium

DevOps / Infrastructure

* Docker
* Linux
* Git

⸻
## Project Structure

```text
UfcDB2/
├── FighterScraper.py          # Scrapes UFC fighter data
├── FightScraper.py            # Scrapes UFC fight data
├── EventScraper.py            # Scrapes UFC event data
├── CREATE_UFCBD2.sql          # Creates the MySQL database schema
├── docker-compose.yml         # Docker configuration
└── README.md
```

⸻

Current Development Status

The data scraping pipelines, database schema, and server infrastructure are functional. Development is currently focused on building the backend API and frontend interface.

⸻

Goals

* Build a scalable UFC statistics platform
* Practice full-stack software engineering
* Learn backend API development and deployment
* Improve experience with Docker and Linux server management
* Explore database design and large-scale sports data organization

⸻

Future Improvements

* Automated scheduled scraping jobs
* User accounts and saved queries
* Better analytics and visualizations
* Public deployment
* API documentation with OpenAPI/Swagger

⸻

Author

Maxime Bouclin

GitHub: github.com/maximebouclin
