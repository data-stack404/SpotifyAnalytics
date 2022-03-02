from flask import Flask, Response
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io


class DBManager:
    def __init__(self, database='spotify_analytics', host="mysql-server", user="test", password="test"):
        self.connection = mysql.connector.connect(
            user=user, 
            password=password,
            host=host,
            database=database,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

    def query_report(self):
        self.cursor.execute('''
                                    SELECT
                                        NR_USERS.day_id,
                                        NR_USERS.active_users,
                                        AVG_LISTENS.avg_listens,
                                        NR_LISTENS.nr_listens
                                        
                                    FROM
                                        (SELECT
                                        day_id,
                                        COUNT(DISTINCT user) AS active_users
                                        FROM spotify_listens
                                        GROUP BY day_id) NR_USERS
                                        JOIN 
                                        (SELECT
                                        day_id,
                                        AVG(nr_listens) as avg_listens
                                        FROM
                                        (
                                        SELECT
                                        day_id,
                                        user,
                                        COUNT(listened_at) as nr_listens
                                        FROM spotify_listens
                                        GROUP BY day_id, user) SUB
                                        GROUP BY day_id) AVG_LISTENS ON NR_USERS.day_id = AVG_LISTENS.day_id
                                        
                                        JOIN
                                        (SELECT
                                        day_id,
                                        COUNT(listened_at) AS nr_listens
                                        FROM spotify_listens
                                        GROUP BY day_id) NR_LISTENS ON NR_USERS.day_id = NR_LISTENS.day_id 
                                      ''', conn)
        table_rows = self.cursor.fetchall()
        return pd.DataFrame(table_rows, columns=self.cursor.column_names)



server = Flask(__name__)
conn = None

@server.route('/report')
def management_report():

    global conn
    if not conn:
        conn = DBManager()
    df = conn.query_report()
    output = df.to_html(classes='management')
    return Response(output, mimetype='text/html')

if __name__ == '__main__':
    server.run
