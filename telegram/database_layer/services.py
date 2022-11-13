from utils.FleissKappa import MyWeightedFleissKappa
from constants import Configs, OutPutMessages
from exceptions import AlreadyHasIntroducer, IntroducerNotFound, YouIntroducedThisUserCanNotBeenIntroducer, \
    UserNotFound, AnsweredBeforeByTheUser, NoQuestionReadyToAnswerWait
from models import User, ColloquialQuestion, UserAnswers


class SqliteQueryServices:

    def register_user(self, message_user, chat_id):
        user: User = User.get_or_create(user_id=message_user.id)[0]
        user.chat_id = chat_id
        user.username = message_user.username.lower()
        user.save()
        return user

    def change_user_channel(self, user_id, channel):
        user: User = User.get_or_create(user_id=user_id)[0]
        user.selected_channel = channel
        user.save()
        return user

    def get_user(self, user_id):
        user = User.get_or_none(user_id=user_id)
        if user:
            return user
        raise UserNotFound()

    def get_user_selected_channel(self, user_id):
        return self.get_user(user_id).selected_channel

    def get_user_score(self, user_id):
        return self.get_user(user_id).score

    # def check_score_for_music(self, user_id):
    #     return self.get_user(user_id).score >= Constants.music_cost

    # def take_score_for_music(self, user_id):
    #     user = self.get_user(user_id)
    #     user.score -= Constants.music_cost
    #     user.save()

    def get_user_introducer(self, user_id):
        return self.get_user(user_id).introducer_username.lower()

    def set_introducer_first_time(self, user_id, introducer_username: str):
        introducer_username = introducer_username.lower()
        user = self.get_user(user_id)
        if not user.introducer_username:
            try:
                introducer_user = User.get(username=introducer_username)
                if introducer_user.user_id == user.user_id:
                    raise Exception()
            except Exception as e:
                raise IntroducerNotFound()
            if introducer_user.introducer_username == user.username:
                raise YouIntroducedThisUserCanNotBeenIntroducer()

            user.introducer_username = introducer_username
            user.save()

            introducer_user.score += Configs.introduce_score
            introducer_user.save()
            return introducer_user
        else:
            raise AlreadyHasIntroducer()

    def create_question(self, request_word, nine_choice_list, nine_choice_score_list=None):
        data = {f"choice{i}": nine_choice_list[i] for i in range(9)}
        if nine_choice_score_list:
            data.update({f"choice{i}_score": nine_choice_score_list[i] for i in range(9)})

        data["choice9"] = OutPutMessages.none_of_the_above_options

        return ColloquialQuestion.get_or_create(request_word=request_word, **data)[0]

    def answer_question(self, question_id, user_id, choice):
        question = ColloquialQuestion.get_by_id(question_id)
        user = self.get_user(user_id)
        if UserAnswers.select().where((UserAnswers.user == user) & (UserAnswers.question == question)).count() == 0:
            answer: UserAnswers = UserAnswers.get_or_create(user=user, question=question, choice=choice)[0]
            answer.choice = choice
            answer.save()

            # add score to use
            user.score += Configs.question_answer_score
            user.save()
        else:
            raise AnsweredBeforeByTheUser()

    def get_question(self, question_id):
        return ColloquialQuestion.get_by_id(question_id)

    def get_question_by_request_word(self, request_word):
        return ColloquialQuestion.get_or_none(request_word=request_word)

    def select_a_new_question_for_user(self, user_id):
        if Configs.DEBUG and not ColloquialQuestion.select().exists():
            self.create_question("test", ["اول", "دوم", "سوم", "چهار", "پنجم", "شیشم", "هفتم", "هشتم", "نهم"])
            self.create_question("test2", ["اول", "دوم", "سوم", "چهار", "پنجم", "شیشم", "هفتم", "هشتم", "نهم"])
        user = self.get_user(user_id)
        answer_subquery = UserAnswers.select().where((UserAnswers.user == user)).join(ColloquialQuestion).select(
            ColloquialQuestion.id).distinct()
        questions = ColloquialQuestion.select().where(
            (ColloquialQuestion.done == False) & (ColloquialQuestion.id.not_in(answer_subquery))).order_by(
            ColloquialQuestion.created_date.asc())
        if questions.exists():
            return questions.first()
        raise NoQuestionReadyToAnswerWait()

    def check_question_update_done_with_final_answer_just_get_done(self, question_id):
        question = ColloquialQuestion.get(id=question_id)
        if question.done:
            return False
        answer_dict = {}
        for answer in question.q_answers:
            answer_dict[answer.choice] = answer_dict.get(answer.choice, 0) + 1
        _, acceptable, selected_options = MyWeightedFleissKappa(answer_dict,
                                                                [question.get_choice_score_by_number(i) for i in
                                                                 range(8)])
        if acceptable:
            question.done = True
            question.user_selected_choice = selected_options
            question.save()
            # handle wrong answers TODO

            return question
        return False

    def get_question_wrong_answers(self, done_question_id):
        question = ColloquialQuestion.get(id=done_question_id)
        if not question.done:
            raise Exception()
        final_option = question.user_selected_choice
        wrong_users = question.q_answers.select().where((UserAnswers.choice == final_option)).select(UserAnswers.user)
        return wrong_users

    def punish_user_with_wrong_answer(self, wrong_user=None, wrong_user_id=None):
        if wrong_user_id:
            wrong_user = self.get_user(wrong_user_id)
        wrong_user.score += Configs.question_wrong_answer_score
        wrong_user.save()


if __name__ == '__main__':
    u = SqliteQueryServices()

    user = u.change_user_channel(45785785, "sdfgsdf")
    res1 = u.get_user_selected_channel(45785785)
    u.change_user_channel(45785785, "sdfgsdf56")
    res2 = u.get_user_selected_channel(45785785)
    print(res1, res2)

    q = u.create_question("test", ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"])
    u.answer_question(q.id, user.user_id, 4)
