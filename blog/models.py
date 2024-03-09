from py2neo import Graph, Node, Relationship, NodeMatcher,RelationshipMatcher
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME', 'neo4j')
password = os.environ.get('NEO4J_PASSWORD', '123456')

# print(url, username, password)
graph = Graph(url + '/db/data/', auth=(username, password))
# graph = Graph(url + '/db/data/', username=username, password=password)

class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        # user = graph.find_one('User', 'username', self.username) # V3 syntax
        # user = graph.nodes.match('User', self.username).first() # V4 syntax

        node_matcher = NodeMatcher(graph)
        user = node_matcher.match("User").where(username=self.username).first()

        return user

    def register(self, password):
        if not self.find():
            user = Node('User', username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        # print(user['password'])
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text):
        user = self.find()
        post = Node(
            'Post',
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )

        rel = Relationship(user, 'PUBLISHED', post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = Node('Tag', name=name)
            tag.__primarykey__ = "name"
            tag.__primarylabel__ = "Tag"
            graph.merge(tag)

            rel = Relationship(tag, 'TAGGED', post)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()
        # post = graph.find_one('Post', 'id', post_id) # V3 syntax
        # post = graph.nodes.match('Post', post_id).first() # V4 syntax

        node_matcher = NodeMatcher(graph)
        post = node_matcher.match("Post").where(id=post_id).first()

        graph.merge(Relationship(user, 'LIKED', post))

    def get_recent_posts(self):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = {username}
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 5
        '''

        return graph.run(query, username=self.username)

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = '''
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        '''

        return graph.run(query, username=self.username)

    def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = '''
        MATCH (they:User {username: {they} })
        MATCH (you:User {username: {you} })
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN SIZE((they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you)) AS likes,
               COLLECT(DISTINCT tag.name) AS tags
        '''

        return graph.run(query, they=other.username, you=self.username).next

def get_todays_recent_posts():
    query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''

    return graph.run(query, today=date())

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')

def seed():

    node_matcher = NodeMatcher(graph)    
    for name in ['Adam', 'Eve', 'Alice', 'Bob']:
        user = node_matcher.match("User").where(username=name).first()
        if not user:
            user = Node('User', username=name, password=bcrypt.encrypt(name))
            graph.create(user)

        post_title = name+' 新人报道'
        post = node_matcher.match("Post").where(title = post_title).first()
        if not post:
            post = Node(
                'Post',
                id=str(uuid.uuid4()),
                title= post_title,
                text='大家好，我是' + name,
                timestamp=timestamp(),
                date=date()
            )

            rel = Relationship(user, 'PUBLISHED', post)
            graph.create(rel)

        graph.merge(Relationship(user, 'LIKED', post))
        
        tag = Node('Tag', name='报道')
        tag.__primarykey__ = "name"
        tag.__primarylabel__ = "Tag"
        graph.merge(tag)
        rel = Relationship(tag, 'TAGGED', post)
        graph.create(rel)



    