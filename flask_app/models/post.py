from flask_app.config.mysqlconnection import connectToMySQL


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.source = data['source']
        self.description = data['description']
        self.content = data['content']
        self.url = data['url']
        self.image = data['image']
        self.published_date = data['published_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save_news(cls, data):
        query = """
        INSERT INTO posts
        (title, source, description, url, image, published_date, user_id)
        VALUES (%(title)s, %(source)s, %(description)s, %(url)s, %(image)s, %(published_date)s, %(user_id)s);
        """
        results = connectToMySQL('news_share').query_db(query, data)
        return results

    @classmethod
    def delete_post(cls, id):
        query = """
        DELETE FROM posts
        WHERE id = %(id)s;
        """
        results = connectToMySQL('news_share').query_db(query, id)
        return results
