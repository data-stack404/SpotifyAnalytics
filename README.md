# SpotifyAnalytics
Sample data pipepline using mocked Spotify data

**Caution: This is just a demo setup - DO NOT use this configuration for production!**

#How to start
1. Clone the repository
2. Open the terminal and cd to the project root
3. copy the "dataset.txt" file into the sub folder "ingestion"
4. verify that you have Python3 + pip installed
5. verify that you have docker + docker compose running
6. (to be sure) run "docker-compose rm -v"
7. run 'docker-compose up --build --remove-orphans --force-recreate'

#Task 1
just run the container and the backend will import messages into our DB
 verify that everything works by connection to the DB:
- docker-compose exec mysql-server /bin/bash
- mysql -utest -ptest
- use spotify_analytics;
- SELECT COUNT(user) as counter from spotify_listens;

#Task 2 - Question 1
- "docker-compose exec mysql-server /bin/bash"
- "mysql -utest -ptest"
- "use spotify_analytics;"
- "SELECT user, COUNT(listened_at) as listens  FROM spotify_listens group by user order by listens DESC FETCH FIRST 10 ROWS ONLY;"

#Task 2 - Question 2
- "SELECT DISTINCT user f rom spotify_listens where day_id = 20190501;"

#Task 2 - Question 3
- "SELECT SUB.user, song, SL.day_id  FROM (SELECT user, MIN(listened_at) as first_listened_at  FROM spotify_listens group by user) SUB JOIN spotify_listens SL ON SUB.user = SL.user AND SUB.first_listened_at = SL.listened_at;"

#Task 3
Open your Browser and go to http://localhost:80/report