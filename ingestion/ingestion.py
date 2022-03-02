import time
import sys
import json
import mysql.connector
import datetime


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

    def create_table(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS spotify_listens (raw_message TEXT, user VARCHAR(200), day_id INT, song TEXT, artist TEXT, album TEXT, listened_at INT, created DATETIME DEFAULT CURRENT_TIMESTAMP)")
            self.cursor.execute("CREATE UNIQUE INDEX spotify_idx ON spotify_listens(user, listened_at)")
            self.connection.commit()
        except:
            return

    def insert_record(self, record_to_insert):
        if record_to_insert:
            try:
                self.cursor.execute('INSERT INTO spotify_listens (raw_message, user, day_id, song, artist, album, listened_at) VALUES ('+record_to_insert['raw_message']+','+record_to_insert['user']+','+record_to_insert['day_id']+','+record_to_insert['song']+','+record_to_insert['artist']+','+record_to_insert['album']+','+record_to_insert['listened_at']+')')
                self.connection.commit()
            except:
                return


def parse_json(line):
    parsed_json = json.loads(line)
    return parsed_json


def sanitize(dirty_string):
    clean_string = '\"' + str(dirty_string) if dirty_string else ""
    return clean_string + '\"'


JSON_DATA_FILE = "dataset.txt"
global db_connection

if __name__ == "__main__":
    time.sleep(10)
    db_connection = None
    if not db_connection:
        db_connection = DBManager()
        db_connection.create_table()

    try:
        json_data_file_handle = open(JSON_DATA_FILE, 'r')

        while True:
            position = json_data_file_handle.tell()
            current_line = json_data_file_handle.readline()

            if not current_line:
                time.sleep(1)
                json_data_file_handle.seek(position)
                continue
            else:
                current_line = current_line.strip()
                parsed_json = parse_json(current_line)
                parsed = {
                    'raw_message': sanitize(current_line.replace("\"", "\\\"")),
                    'user': sanitize(parsed_json['user_name']),
                    'day_id': sanitize(datetime.datetime.fromtimestamp(parsed_json['listened_at']).strftime('%Y%m%d')),
                    'song': sanitize(parsed_json['track_metadata']['track_name']),
                    'artist': sanitize(parsed_json['track_metadata']['artist_name']),
                    'album': sanitize(parsed_json['track_metadata']['release_name']),
                    'listened_at': sanitize(parsed_json['listened_at'])
                }

                if len(current_line) > 0:
                    db_connection.insert_record(record_to_insert=parsed)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        json_data_file_handle.close()
        sys.exit()
