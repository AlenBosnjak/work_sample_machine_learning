# Overview
In this project an approach for the prediction of football matches is developed. For this purpose, three data sets were created and their impact on the accuracy of the predictions is considered. An artificial neural network is developed for each data set. Both the hyperparameter optimization and the training of the networks take place under the same conditions. The Project was divided into three parts which will be described in the following.

:warning:  (warning)  
This project was developed under great time pressure. A total of nine weeks were available for the bachelor thesis. Therefore, the full nine weeks could not be used for programming. The code needs refactoring before further use for example there are duplicates in the code but also the structure needs to be modified.  

# 1.Gathering and storing the data
In order to collect the required data an API which provides general data about the matches, player performances and line-ups was used. The dataset contains data from seven football leagues and six seasons. The responses were then combined into larger JSON files. Due to inconsistencies in the provided data it was necessary to extract the data from the JSON-files manually and to store it in an own database schema.

The requests to the API can be found under :arrow_right: **API Requests**  
Extraction from the JSON files can be found under :arrow_right: **json_to_db**  

# 2.Reshape and model the data
The data is processed into features such as player ratings and team ratings. After calculating these features, the data is saved as csv files.
Calculation of the features can be found under :arrow_right: **notebooks**  
Used Features were:  
* Elo-rating which rates the strength of the team.
* Offesnive and defensive ratings of the teams.
* Player ratings which are based on profiles of the positions:
  * Goalkeeper
  * Defensive
  * Midfielder
  * Forward
  
# 3.Train the neural network
After creating the three datasets the Models were trained and the best model(no_players.ipynb) reached an accuracy of 53% on the validation set. The goal was the classification of a match into one of the three classes "Heim", "Auswärts" and "Remis" which translate to "home", "away", "draw".

The validation and building of the neural networks can be found under :arrow_right: **tensorflow**
