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
    choice0_score = DoubleField(default=0.1, null=False)
    choice1 = CharField()
    choice1_score = DoubleField(default=0.1, null=False)
    choice2 = CharField()
    choice2_score = DoubleField(default=0.1, null=False)
    choice3 = CharField()
    choice3_score = DoubleField(default=0.1, null=False)
    choice4 = CharField()
    choice4_score = DoubleField(default=0.1, null=False)
    choice5 = CharField()
    choice5_score = DoubleField(default=0.1, null=False)
    choice6 = CharField()
    choice6_score = DoubleField(default=0.1, null=False)
    choice7 = CharField()
    choice7_score = DoubleField(default=0.1, null=False)
    choice8 = CharField()
    choice8_score = DoubleField(default=0.1, null=False)
    choice9 = CharField()
    choice9_score = DoubleField(default=0.1, null=False)

    done = BooleanField(default=False)
    user_selected_choice = SmallIntegerField(null=True)

    def get_choice_by_number(self, i):
        return getattr(self, f"choice{i}")

    def set_choice_by_number(self, i, value):
        return setattr(self, f"choice{i}", value)

    def get_choice_score_by_number(self, i):
        return getattr(self, f"choice{i}_score")

    def set_choice_score_by_number(self, i, value):
        return setattr(self, f"choice{i}_score", value)


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
