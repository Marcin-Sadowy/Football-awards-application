# Football-awards-application

**Overview**

The project is a web application that automatically chooses the award winners for different football tournaments (World Cups, Euros etc.) based on match statistics.

The application calculates who should win a particular award using a weighted scoring system. The user can adjust which metrics (goals, assists etc.) should have the biggest impact in calculating scores for different players. Additonally, the user can create their own custom awards, define which statistics are the most important and see the rankings of top players with respect to that award. The app gives a thorough overview of the reasons for shoosing award winners along with interactive plots used to compare different players or see the influence of different metrics.

**Goal**

The goal of the project is to simulate the development lifecycle of a simple web application. It combines data science, software engineering, web design and containerization. 

**Project components**

- data collection and processing
- database design
- backend API for connecting the app to the database and engine
- weighted-score algorithm implementation
- data analytics
- containerization

**Planned features**

- import tournament and match statistics
- weighted scoring system which the user can alter
- ranking generation
- explanations of the results of rankings with interactive plots
- golden ball award (for best all-around player)
- golen glove award (for best goalkeeper)
- tournament best 11 team with user-selected formation
- filtering (for example disable penalties or count only play-off matches)
- custom awards created by the user
