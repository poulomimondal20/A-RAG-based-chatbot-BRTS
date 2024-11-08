# Task 2: Data Collection for AI Chatbot - BRTS Navigation in Bhopal

## Overview
Task 2 of our project focused on gathering and structuring critical data regarding bus stations, routes, and geographical coordinates (latitude and longitude). This data served as the foundation for the AI chatbot, enabling it to assist users in navigating the Bhopal BRTS system efficiently.

## Key Data Collected
- **Station Names**: A comprehensive list of all Bhopal BRTS stations was collected.
- **Route Information**: Details of the routes, including start and end stations, intermediate stops, and route numbers, were gathered.
- **Latitude and Longitude**: Geographical coordinates for each station were collected to assist with mapping and route visualization.

## Dataset and Route Categories
The dataset was divided into two main route categories:
- **Trunk Routes (TR)**: Major routes connecting important stations.
- **Standard Routes (SR)**: Other routes connecting smaller stations and areas.

Key data points in the dataset included:
- **Latitude** and **Longitude** for each station, which were crucial for distance and time calculations.
- The **Haversine formula** was discussed as a method to measure distances between stations for better route recommendations.

## Group Contributions

### Group 1: RAG System
Group 1, led by **Arihant**, focused on developing and documenting the Retrieval-Augmented Generation (RAG) system.
- They were in the learning phase and made initial contributions towards setting up the RAG model.
- The group faced challenges with computational requirements while using cloud-based LLM models.
- They explored alternative solutions, including Hugging Face models and OpenAI APIs, to reduce system load and improve efficiency.
- As the project progressed, Group 1 also began discussions on integrating the dataset into the RAG system, planning to incorporate real-time transit data using APIs.
- **Group 3 merged with Group 1** to streamline efforts and improve coordination between the groups.

### Group 2: LSTM Models
Group 2, led by **Saransh**, worked on developing LSTM models for the chatbot.
- They were provided with a research paper suggesting a simpler version of LSTM that would allow for better fine-tuning and performance.
- The group identified additional resources tailored to the project’s transportation requirements, especially around handling structured queries like schedules and routes.
- They initiated discussions around integrating a database to support the chatbot functionalities, enabling efficient management of route data and queries.
- They also planned for future enhancements that would involve improving the chatbot’s ability to answer questions related to specific routes and travel times.

## Future Enhancements and Map Visualization
- The **Haversine formula** was planned to be implemented to calculate distances between stations, allowing users to get accurate route suggestions.
- **PyDeck** charts were explored for **map visualization**, displaying station locations and routes interactively within the chatbot interface.

## Real-Time Data Integration
In the future, the team planned to:
- Use the **Open Street Map API** to gather real-time travel times for bus routes, enhancing the chatbot’s ability to provide up-to-date transit information.
- **Database integration** for the chatbot’s functionalities was being explored, particularly to improve the chatbot’s ability to manage and retrieve route information efficiently.

## Challenges Encountered
- **Computational Resources**: Group 1 (working on the RAG model) faced challenges with computational requirements when using cloud-based LLM models. Alternative solutions, such as using Hugging Face models or OpenAI APIs, were explored to optimize the process.