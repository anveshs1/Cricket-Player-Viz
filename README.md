# Cricket-Player-Viz-private
# Cricket-Player-Basic-Visualization
Basic visualizations of some random cricket players from all international teams

### Description

The espncricinfo.com site provides numeral details of cricket matches and series - live, past and also detailed scorecards of each induvidual match.
Cricket-Player-Basic-Visualization Dashboard is a project built using Plotly's Dash, Beautiful soup, Pandas in python. Using Data from cricinfo
about induvidual players, it tries to present their batting/bowling statistics using simple figures - bar plots and scatter plots.
Disclaimer: This  is not intended for commercial use and neither it nor its creator has any affiliation with ESPNCricInfo. The [LICENSE](LICENSE.txt) for this library applies only to the code, not to the data.
 It is a work in progress, and bug reports and feature requests are welcome.


### Usage

#### source the required modules.
```python
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import logging
import datetime
import uuid
import json
from scrape_players import get_players, get_player_stats_dfs
from lookups import countries,cols
from parse_player_data import induv_stats
```

1) The first function to be used is 'get_players'.Passing a country name to it returns a dictionary with the 'playername' as key and corresponding
'pid' as its value. EX: For country 'england', the result is a dictionary with all the players in the below url.
https://www.espncricinfo.com/player/team/england-1
NOTE: It only picks the players loaded in the current page and doesn't scroll the page to get the full list.

```python
get_players('england')
england https://www.espncricinfo.com/player/team/england-1
2021-09-17 14:12:48.428 DEBUG:	Starting new HTTPS connection (1): www.espncricinfo.com:443
2021-09-17 14:12:48.838 DEBUG:	https://www.espncricinfo.com:443 "GET /player/team/england-1 HTTP/1.1" 200 None
{'Moeen Ali': 8917, 'James Anderson': 8608, 'Jofra Archer': 669855, 'Jonny Bairstow': 297433, 'Tammy Beaumont': 297074, 'Dom Bess': 646847, 'Sam Billings': 297628, 'Maia Bouchier': 1022077, 'James Bracey': 747031, 'Stuart Broad': 10617, 'Katherine Brunt': 53906, 'Rory Burns': 398778, 'Jos Buttler': 308967, 'Brydon Carse': 596417, 'Zak Crawley': 665053, 'Kate Cross': 297085, 'Sam Curran': 662973, 'Tom Curran': 550235, 'Freya Davies': 652945, 'Charlotte Dean': 1039421, 'Sophia Dunkley': 885815, 'Sophie Ecclestone': 878039, 'Georgia Elwiss': 297036, 'Tash Farrant': 580663, 'Ben Foakes': 364788, 'Sarah Glenn': 885837, 'Lewis Gregory': 362201, 'Haseeb Hameed': 632172, 'Amy Jones': 515874, 'Chris Jordan': 288992, 'Heather Knight': 358259, 'Emma Lamb': 749957, 'Dan Lawrence': 641423, 'Jack Leach': 455524, 'Liam Livingstone': 403902, 'Saqib Mahmood': 643885, 'Dawid Malan': 236489, 'Eoin Morgan': 24598, 'Craig Overton': 464626, 'Matt Parkinson': 653695}
get_players('india')
india https://www.espncricinfo.com/player/team/india-6
2021-09-17 14:12:58.211 DEBUG:	Starting new HTTPS connection (1): www.espncricinfo.com:443
2021-09-17 14:12:58.637 DEBUG:	https://www.espncricinfo.com:443 "GET /player/team/india-6 HTTP/1.1" 200 None
{'Mayank Agarwal': 398438, 'Ravichandran Ashwin': 26421, 'Simran Bahadur': 1204925, 'Taniya Bhatia': 883423, 'Ekta Bisht': 442048, 'Jasprit Bumrah': 625383, 'Yuzvendra Chahal': 430246, 'Deepak Chahar': 447261, 'Rahul Chahar': 1064812, 'Harleen Deol': 960845, 'Shikhar Dhawan': 28235, 'Ruturaj Gaikwad': 1060380, 'Rajeshwari Gayakwad': 709635, 'Richa Ghosh': 1212830, 'Jhulan Goswami': 53932, 'Krishnappa Gowtham': 424377, 'Dayalan Hemalatha': 961107, 'Ishan Kishan': 720471, 'Shreyas Iyer': 642519, 'Ravindra Jadeja': 234675, 'Mansi Joshi': 960815, 'Harmanpreet Kaur': 372317, 'Virat Kohli': 253802, 'Kuldeep Yadav': 559235, 'Bhuvneshwar Kumar': 326016, 'Smriti Mandhana': 597806, 'Mohammed Shami': 481896, 'Mohammed Siraj': 940973, 'Shahbaz Nadeem': 31872, 'T Natarajan': 802575, 'Devdutt Padikkal': 1119026, 'Manish Pandey': 290630, 'Shikha Pandey': 442145, 'Hardik Pandya': 625371, 'Krunal Pandya': 471342, 'Rishabh Pant': 931581, 'Nuzhat Parween': 960973, 'Axar Patel': 554691, 'Monica Patel': 1213438, 'Poonam Yadav': 630972}
```

2) 'get_player_stats_dfs' returns the dataframe 'induv_stat' which has induvidual match statistics(runs,wickets,catches etc..)
for all the matches a player has played in all formats of the game.

Arguments:  

            countryname - country name
            players - dictionary of player,pids of a particular country - if defined uses the existing values
                        else the output of 'get_players' function
            pid - playerid of the player
            wtf - Write to File - False by defualt. (if true, exports the dataframe to a csv file in Data directory)
This uses the function 'induv_stats' inside 'parse_player_data' to clean up the dataframe so that
it is consistent for all players.

```python
get_player_stats_dfs('england', players, pid=8917, wtf=False)
england https://www.espncricinfo.com/player/team/england-1
2021-09-17 14:22:27.044 DEBUG:	Starting new HTTPS connection (1): www.espncricinfo.com:443
2021-09-17 14:22:27.497 DEBUG:	https://www.espncricinfo.com:443 "GET /player/team/england-1 HTTP/1.1" 200 48743
{'Moeen Ali': 8917}
2021-09-17 14:22:31.201 DEBUG:	  Bat1 Bat2 Runs Wkts  ...          Opposition       Ground   Start Date  Unnamed: 11
0   44    -   44    1  ...   ODI v West Indies  North Sound  28 Feb 2014   ODI # 3477
1   10    -   10    1  ...   ODI v West Indies  North Sound   2 Mar 2014   ODI # 3480
2   55    -   55    1  ...   ODI v West Indies  North Sound   5 Mar 2014   ODI # 3484
3    5    -    5    -  ...  T20I v West Indies   Bridgetown  11 Mar 2014   T20I # 362
4    3    -    3    -  ...  T20I v West Indies   Bridgetown  13 Mar 2014   T20I # 364
[5 rows x 12 columns]
```
NOTE: For newer players where the induvidual match statistics are not available at cricinfo, the dashboard
        returns empty figures.

        EX players: {'Harmanpreet Kaur': 372317} - India
                    {'Nicola Carey': 381217} - Australia 
                    {'Katherine Brunt': 53906} - England


3) The 'lookups' file has the below dictionaries that are used by other functions.


    countries
    matches
    cols

 ### Dashboard
The dashboard 'Cricket-Players-Basic-Viz' shows basic plots of cricket players from a list of players obtained from cricinfo
using 2 bar plots and 2 scatter plots. The 2 bar plots - one for 'Total Runs' and the other 'Total Wickets' shows the total count of
runs/wickets a player has scored each year. The data is split according to Matchtype(ODI/Test/T20). The 2 scatter plots show the
runs/wickets a player has scored in each of the matches played(actively). Each data point on hover shows the Runs/Wkts/year/oppo
sition. The data points in the figures can be zoomed in/panned as needed interactively. When the dashboard is opened the first time,
it defualts to Indian player 'Virat Kohli'. Users can select any available country and this refreshes the players available for
it. When a specific player is selected, the data for the select player is fetched and their graphs updated!

The app can be tested at https://cricket-player-viz.azurewebsites.net/





### Requirements

See requirements.txt


