# MyBudgetTrackr



#### Description:
**MyBudgetTrackr** is a personal finance management tool that I developed as part of my final project for Harvard’s CS50 course. This project is designed to help users manage their finances more effectively by tracking income, expenses, and savings goals in one place. The aim is to provide an intuitive and user-friendly platform to assist individuals in achieving financial stability and reaching their goals.

---

## Key Features

1. **Track Income and Expenses**  
   Users can easily input their income and expenses, which are tracked and summarized for better management. This feature enables users to monitor their financial activity in real time.

2. **Set and Monitor Savings Goals**  
   The app allows users to set savings goals, helping them plan for future expenses or build emergency savings. Users can compare their progress to their goal, which is dynamically updated.

3. **Generate Financial Reports**  
   Users can generate financial reports in PDF format to view their progress over time. These reports include a breakdown of income, expenses, savings, and a graphical representation of financial data.

4. **View Spending Breakdown by Category**  
   Users can get a detailed breakdown of their spending by category, providing them insights into where they can cut back or allocate funds more efficiently.

---

## Technologies Used

- **Python**  
  The backend of the application is built using Python and Flask, a lightweight web framework. Flask was chosen because it allows quick setup and easy integration with the SQLite database.

- **SQLite**  
  The app uses SQLite to store user data, including income, expenses, savings goals, and recurring expenses. This database system is efficient and lightweight, making it a good fit for the app.

- **HTML/CSS**  
  The frontend is built using HTML and CSS, which allows for a simple, yet attractive user interface. The design is optimized for desktop usage, but future updates will focus on making it mobile-friendly.

---

##Steps to Launch##

###Clone the Repository###
```bash
git clone https://github.com/Lietavkin/budgeting_app.git
cd budgeting_app
Set Up a Virtual Environment (Optional)
bash

##For Linux/Mac##
python3 -m venv venv
source venv/bin/activate

##For Windows##
python3 -m venv venv
venv\Scripts\activate
## Install Dependencies
bash

##pip install -r requirements.txt##
Run the App
bash

##flask run##
Access the app in your browser at http://127.0.0.1:5000.

##Future Enhancements##
Data Visualization Enhancements
I plan to enhance the app’s data visualization capabilities, adding more interactive charts and graphs that will allow users to gain deeper insights into their spending patterns and financial habits.

##Email Alerts for Financial Milestones##
As an additional feature, I am considering adding email alerts for when users approach or reach financial milestones, such as hitting their savings goal or exceeding their monthly budget. This feature will keep users engaged and motivated to meet their financial goals.

## Design and Implementation#
The app’s design focuses on simplicity and ease of use, ensuring that users can quickly navigate through different sections. The dashboard provides a snapshot of income, expenses, and savings, while the detailed views of income and expenses allow users to manage their finances at a granular level.

##The app has been developed using the principles of good software design, ensuring that the code is clean, modular, and maintainable. While Flask and SQLite were chosen due to their simplicity and speed, future plans include exploring more advanced technologies to further scale the app’s features and capabilities.

##Conclusion##
Building MyBudgetTrackr has been an excellent learning experience. It allowed me to apply what I’ve learned throughout CS50, from web development to database management. The project also provided an opportunity to explore some areas of personal interest, such as personal finance management, and gave me a chance to build something that can help others better manage their money.

This app is a testament to the skills I’ve acquired during CS50, and I’m excited to continue improving and adding new features. My next steps will focus on making the app more mobile-friendly and enhancing its security with user authentication.

