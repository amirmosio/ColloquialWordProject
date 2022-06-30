from models import User, ColloquialQuestion, UserAnswers


class SqliteQueryServices:
    def change_user_channel(self, chat_id, channel):
        user: User = User.get_or_create(chat_id=chat_id)[0]
        user.selected_channel = channel
        user.save()
        return user

    def get_user_selected_channel(self, chat_id):
        return User.get(chat_id=chat_id).selected_channel

    def create_question(self, request_word, nine_choice_list):
        choices = {f"choice{i}": nine_choice_list[i - 1] for i in range(1, 10)}
        return ColloquialQuestion.get_or_create(request_word=request_word, **choices)[0]

    def answer_question(self, question_id, chat_id, choice):
        question = ColloquialQuestion.get_by_id(question_id)
        user = User.get(chat_id=chat_id)
        if UserAnswers.select().where((UserAnswers.user == user) & (UserAnswers.question == question)).count() == 0:
            answer: UserAnswers = UserAnswers.get_or_create(user=user, question=question, choice=choice)[0]
            answer.choice = choice
            answer.save()
        else:
            raise Exception("Answered before")

    def check_if_question_is_done(self, question_id):
        # TODO
        pass





if __name__ == '__main__':
    u = SqliteQueryServices()

    user = u.change_user_channel("sdfsdf", "sdfgsdf")
    res1 = u.get_user_selected_channel("sdfsdf")
    u.change_user_channel("sdfsdf", "sdfgsdf56")
    res2 = u.get_user_selected_channel("sdfsdf")
    print(res1, res2)

    q = u.create_question("test", ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"])
    u.answer_question(q.id, user.chat_id, 4)
