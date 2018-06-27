# Wanda

## Summary

**Wanda** is a mindfulness tracker focused on improving a user's overall happiness and well-being.  It is inspired by a study by Harvard professor Daniel Gilbert, which revealed that humans mind-wander (think about something other than what they're doing) nearly half of the time, and are significantly less happy when doing so. Wanda reminds users to focus on the present and gathers mind wandering and happiness data through text surveys sent throughout the day. The data is then used to create charts for the user to visualize the impact that mind wandering has on happiness with the goal of decreasing this habit over time.

## About the Developer

Wanda was created by Amee Li, a software engineer in San Francisco. Learn more about her on [LinkedIn](https://www.linkedin.com/in/ameeli/).

## Technologies

**Tech Stack:**

- Python
- Flask
- SQLAlchemy
- Jinja2
- D3
- HTML
- CSS
- Javascript
- JQuery
- AJAX
- JSON
- Twilio API

Wanda is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. The front end templating uses Jinja2, the HTML was built using Bootstrap, and the Javascript uses JQuery and AJAX to interact with the backend. The graphs are rendered using the D3 library. Texts interactions are created with through the Twilio API.

## Features

Wanda will check in by text message throughout the day and ask 2 questions: 
1. Were you mind wandering? 
2. On a scale of 1-10, how are you feeling?

The data gathered from the text surveys is then visualized for the user in these responsive charts, generated using D3. Results can be filtered by time intervals (daily, weekly, monthly, all time).

![alt text](https://github.com/ameeli/wanda/blob/master/src/static/img/wanda-donut.png)

![alt text](https://github.com/ameeli/wanda/blob/master/src/static/img/wanda-graphs.png)

## For Wanda 2.0

- **Goals:** Users can set goals for reducing mind wandering and be rewarded for reaching them.
- **Password hashing:** Hash passwords before saving to database.
- **Survey:** Add additional productivity questions to text survey so users can see their optimal work times.
