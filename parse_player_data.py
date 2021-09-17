import numpy as np
import pandas as pd
from lookups import cols
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# logging.disable(logging.CRITICAL)  # --- disable logging

# Cricinfo html link for Player Ganguly includes all round analysis for tests/odis/20-20's
"""
url = ('https://stats.espncricinfo.com/ci/engine/player/28779.html?class=11;'
        'result=1;result=2;result=3;result=4;result=5;template=results;type=allround;view=match')
df = pd.read_html(url)
"""


def induv_stats(df: list) -> pd.DataFrame:
    """
    This dataframe is used to store runs/wickets/catches in all the matches a player has played in 3
    formats of cricket - Odi/Test/20-20
    :type df: df
    """
    induv_stat = df[3]
    induv_stat_pre = df[2]
    logging.debug(induv_stat.head())
    if induv_stat_pre.shape != (1, 1):
        try:
            induv_stat.drop('Unnamed: 7', axis=1, inplace=True)
        except:
            pass
        induv_stat.rename(columns={induv_stat.columns[-1]: 'Matchno', 'Start Date': 'Startdate'}, inplace=True)
        induv_stat['Startdate'] = pd.to_datetime(induv_stat['Startdate'], format='%d %b %Y')
        try:
            induv_stat['Runs'] = pd.to_numeric(induv_stat['Runs'].replace("-", 0), errors='raise')
        except:
            induv_stat['Runs'] = pd.to_numeric(induv_stat['Bat1'].replace("-", 0), errors='coerce')
            induv_stat.loc[:, 'Runs'].fillna(value=0, inplace=True)
        try:
            induv_stat['Wkts'] = pd.to_numeric(induv_stat['Wkts'].replace("-", 0), errors='raise')
        except:
            induv_stat['Wkts'] = 0
        try:
            conditions = [
                induv_stat.Matchno.str.startswith('ODI'),
                induv_stat.Matchno.str.startswith('Test'),
                induv_stat.Matchno.str.startswith('T20I')]
            choices = ['ODI', 'Test', 'T20I']
            induv_stat['MatchType'] = np.select(conditions, choices, default=np.nan)
        except:
            induv_stat.rename(columns={'Unnamed: 9': 'Matchno'}, inplace=True)
            induv_stat['MatchType'] = np.where(induv_stat.Matchno.str.startswith('ODI'), 'ODI', 'Test')
        induv_stat['year'] = induv_stat['Startdate'].dt.year
    else:
        induv_stat = pd.DataFrame(columns=cols)
    return induv_stat


if __name__ == '__main__':
    pass

