import datetime

from peewee import *

user_database = SqliteDatabase('peewee_database.db')


class BaseModel(Model):
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = user_database


class ColloquialQuestion(BaseModel):
    id = AutoField()
    request_word = CharField()
    choice0 = CharField()
    choice1 = CharField()
    choice2 = CharField()
    choice3 = CharField()
    choice4 = CharField()
    choice5 = CharField()
    choice6 = CharField()
    choice7 = CharField()
    choice8 = CharField()
    done = BooleanField(default=False)
    user_selected_choice = SmallIntegerField(null=True)

    def get_choice_by_number(self, i):
        return getattr(self, f"choice{i}")


class User(BaseModel):
    user_id = BigIntegerField(unique=True, primary_key=True)
    chat_id = CharField(null=True)
    username = CharField(null=True)
    selected_channel = CharField(null=True)
    score = IntegerField(default=0)
    introducer_username = CharField(null=True)


class UserAnswers(BaseModel):
    user = ForeignKeyField(User, backref='u_answers')
    question = ForeignKeyField(ColloquialQuestion, backref='q_answers')
    choice = SmallIntegerField()  # 0, ..., 9


user_database.connect()
user_database.create_tables([User, ColloquialQuestion, UserAnswers])
