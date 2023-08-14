from flask_app.config.mysql_connection import connect_to_mysql
from flask import flash

DATABASE = "private_wall_db"


class Message:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.message = data["message"]
        self.user_id = data["user_id"]
        self.friend_id = data["friend_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO messages (message, user_id, friend_id)
                VALUES ( %(message)s, %(user_id)s, %(friend_id)s );
                """
        results = connect_to_mysql(DATABASE).query_db(query, data)
        return results

    @classmethod
    def get_all(cls, user_id):
        query = """
                SELECT * FROM messages
                LEFT JOIN users ON messages.user_id = users.id 
                WHERE friend_id = %(user_id)s;
                """
        data = {"user_id": user_id}
        results = connect_to_mysql(DATABASE).query_db(query, data)
        messages = []
        for message in results:
            messages.append(Message(message))
        return messages

    @classmethod
    def get_count(cls, user_id):
        query = """
                SELECT COUNT(message) AS count FROM messages
                WHERE friend_id = %(user_id)s;
                """
        data = {"user_id": user_id}
        results = connect_to_mysql(DATABASE).query_db(query, data)
        return results

    @classmethod
    def get_sent_count(cls, user_id):
        query = """
                SELECT COUNT(message) AS count FROM messages
                WHERE user_id = %(user_id)s;
                """
        data = {"user_id": user_id}
        results = connect_to_mysql(DATABASE).query_db(query, data)
        return results

    @classmethod
    def delete(cls, message_id):
        query = "DELETE FROM messages WHERE id = %(message_id)s;"
        data = {"message_id": message_id}
        connect_to_mysql(DATABASE).query_db(query, data)
        return
