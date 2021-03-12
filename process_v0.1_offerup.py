import pandas as pd


def clean_title(data):
    """
    purpose to remove not relevant items like xbox, iphone 8 and so on
    :param data: the original dataframe
    :return: new dataframe
    """
    def dealer_title(series):
        series = series.lower()
        key_words = ['iphone x', 'iphonex']
        if series.find(key_words[0]) == -1 and series.find(key_words[-1]) == -1:
            return -1
        return 1

    def dealer_price(series):
        if series == 'Sold!':
            return -1
        return 1

    assert isinstance(data, pd.DataFrame)
    info_tit = data['Title'].apply(dealer_title)
    info_tit = info_tit[info_tit == -1].index.tolist()
    data = data.drop(axis=0, index=info_tit, inplace=False)

    info_pri = data['Price'].apply(dealer_price)
    info_pri = info_pri[info_pri == -1].index.tolist()
    data = data.drop(axis=0, index=info_pri, inplace=False)

    data = data.reset_index(drop=True)
    return data

def compare_csv(data_yst,data_td):
    '''
    Comparing two csv file from two consecutive days to get new and sold post
    
    :param yst: yesterday's scraping data
    :type yst: pd.DataFrame
    :param td: today's scraping data
    :type td: pd.DataFrame
    
    :return sold: the number of sold items
    :return new: the number of new items
    '''
    
    sold = 0
    new = 0
    
    ID_yst = data_yst['Item ID']
    ID_td = data_td['Item ID']
    
    for item in ID_td:
        if item not in ID_yst.values:
            new += 1
        
    for item in ID_yst:
        if item not in ID_td.values:
            sold += 1
        
    return sold, new

def compute_avg(df):
    '''
    Calculate the average price per type of conditions.
    
    :param df: input pandas dataframe for scraping of one day
    :type df: pd.DataFrame
    
    :return: average price for each condition
    '''
    s1 = df['Condition']
    s2 = df['Price'].astype('float32')
    avg = s2.mean()
    df = pd.concat([s1, s2], axis=1)
    grp = df.groupby(['Condition'])
    composition = s1.value_counts()
    composition.to_csv('composition_of_condition.csv')
    condition_avg = grp.mean()
    condition_avg.to_csv('avg_price_for_conditions.csv')
    return avg, condition_avg



file = './old_scrap/IPhoneX_2019-11-21 19:28:16.667516_Result_Offerup.csv'
df = pd.read_csv(file)
df.drop(axis=1, columns='Unnamed: 0', inplace=True)
df = clean_title(df)
avg, conditional_avg = compute_avg(df)
print(avg)
print(conditional_avg)
#print(df['Title'])