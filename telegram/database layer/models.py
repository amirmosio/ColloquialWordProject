import datetime

from peewee import *

db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class User(BaseModel):
    chat_id = CharField(unique=True, primary_key=True)
    selected_channel = CharField(null=True)


class ColloquialQuestion(BaseModel):
    id = AutoField()
    request_word = CharField()
    choice1 = CharField()
    choice2 = CharField()
    choice3 = CharField()
    choice4 = CharField()
    choice5 = CharField()
    choice6 = CharField()
    choice7 = CharField()
    choice8 = CharField()
    choice9 = CharField()
    done = BooleanField(default=False)
    user_selected_choice = SmallIntegerField(null=True)

    def get_choice_by_number(self, i):
        return getattr(self, f"choice{i}")


class UserAnswers(BaseModel):
    user = ForeignKeyField(User, backref='u_answers')
    question = ForeignKeyField(ColloquialQuestion, backref='q_answers')
    choice = SmallIntegerField()  # 0, ..., 10


db.connect()
db.create_tables([User, ColloquialQuestion, UserAnswers])
