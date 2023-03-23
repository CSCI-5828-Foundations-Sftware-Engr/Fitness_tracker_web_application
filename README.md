# Fitness_tracker_web_application
One application to track all your activities and stay fit
<p align="center">
  <img src="Architecture_Diagram.png" alt="alt text" width="500" style="margin-bottom: 20px;" />
</p>
In this architecture, React.js is used for the frontend, Python and Flask are used for the backend, and MongoDB is used as the database. The external API sends requests to the backend, which is responsible for processing the requests and communicating with the database.

When a user accesses the fitness tracker web application through their browser, the frontend built with React.js sends requests to the backend REST API, which communicates with the MongoDB database to retrieve or store data related to the user's fitness activities.

The backend is responsible for processing requests from the frontend and communicating with the database to retrieve or store data. In addition, the backend communicates with the external API to retrieve relevant fitness data, such as the user's daily steps and calories burned.

The MongoDB database stores all the data related to the user's fitness activities, including their goals, progress, and achievements.

Heroku, a cloud platform, is used to host the fitness tracker web application. Heroku provides a scalable and secure infrastructure for the application to run on, and it can handle large amounts of traffic without any downtime.

Overall, this architecture provides a robust and scalable platform for a fitness tracker web application, allowing users to track and monitor their fitness activities, set goals, and view their progress over time.
