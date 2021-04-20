import os
import psycopg2
import datetime
import pandas as pd
import pandas.io.sql as psql
from get_moving_avg import sma, ema, wma

def heroku_eda():

    # Setup connection with DB
    pg_auth = os.environ.get("PG_AUTH")

    conn = psycopg2.connect(host="localhost",
                            user="postgres",
                            dbname="investment_db",
                            password=pg_auth)

    cur = conn.cursor()
    cur.execute("SELECT * FROM stock_price")
    rows = cur.fetchall()

    # Query data
    df = psql.read_sql('select * from stock_price', conn)
    df_high = psql.read_sql('''
                            select
                            	distinct a.date::date,
                            	name,
                            	high,
                                low,
                                open,
                                close
                            from
                            	(
                            		select
                            			distinct date,
                            			name,
                            			price,
                            			max(price) over(partition by date::date, name) as high,
                            			min(price) over(partition by date::date, name) as low,
                            			first_value(price) over(partition by date::date, name order by date::date asc) as open,
                            			last_value(price) over(partition by date::date, name order by date::date asc) as close
                            		from stock_price
                            	) a
                            order by 1
                            ''', conn)

    return df_high

# Get dataframe for moving average
def get_ma_df(data, colName, period_1, period_2):

    data.loc[:,'sma_{}'.format(period_1)] = sma(data, colName, period_1)
    data.loc[:,'sma_{}'.format(period_2)] = sma(data, colName, period_2)

    data.loc[:,'ema_{}'.format(period_1)] = ema(data, colName, period_1)
    data.loc[:,'ema_{}'.format(period_2)] = ema(data, colName, period_2)

    data.loc[:,'wma_{}'.format(period_1)] = wma(data, colName, period_1)
    data.loc[:,'wma_{}'.format(period_2)] = wma(data, colName, period_2)

    data = data.iloc[period_2+1:]

    return data
