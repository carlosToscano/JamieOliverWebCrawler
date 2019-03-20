# JamieOliverWebCrawler
crawls through Jamie Oliver´s website and inserts recipes into a database.
-First Step: get all teh data
-Second Step: build a website to filter by ingredient
-Third Step: cleanup DB and improve DB

-Problems I am finding:
*Resolution

-On an error, application can't recover
*Too much recursion. I need a small project to save&recover the state of web crawlers in a simple manner, for wich I will remove recursion from the logic. This can allow also multiple workers.

-Information missing from pages
*Fix the code when exception arises

-Stupid values like an ingredient called "TAMPER"
*After getting everything I will cleanup the DB (script or manual)

-Firewall blocks us dor DDos attack
*1) on 403 notify AWS SNS; a lambda will restart the container to change IP
*2) on 403 notify AWS SNS; a lambda will change the proxy o the EC2
*3) on 403 requests uses a different proxy
