
# neo4j-flask

This project is based on https://github.com/nicolewhite/neo4j-flask/ (which stops maintainence). 

Main revision points:

1. Support new versions of py2neo
2. Add `models.seed()` to populate the db with sample data.

A microblog application written in Python powered by Flask and Neo4j. 
Tutorial: https://nicolewhite.github.io/neo4j-flask/

## How to run

On windows, start the neo4j service: 
```
C:\Windows\System32>neo4j.bat console
2024-03-08 14:13:55.971+0000 INFO  ======== Neo4j 3.5.5 ========
2024-03-08 14:13:55.983+0000 INFO  Starting...
2024-03-08 14:13:59.995+0000 INFO  Bolt enabled on 127.0.0.1:7687.
2024-03-08 14:14:01.502+0000 INFO  Started.
2024-03-08 14:14:02.397+0000 INFO  Remote interface available at http://localhost:7474/
```

Optionally, set environment variables `NEO4J_USERNAME` and `NEO4J_PASSWORD`
to your username and password, respectively:**
```
$ export NEO4J_USERNAME=neo4j
$ export NEO4J_PASSWORD=123456
```
Or, set `dbms.security.auth_enabled=false` in `conf/neo4j-server.properties`.

Then:

```
git clone https://github.com/zhangys11/neo4j-flask.git
cd neo4j-flask
pip install -r requirements.txt
python run.py
```
Open [http://localhost:5000](http://localhost:5000).  
You can also check the [neo4j admin panel](http://localhost:7474) to see the populated data 
