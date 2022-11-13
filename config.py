import torch


class Configs:
    DEBUG = False
    question_answer_score = 1
    question_wrong_answer_score = -5
    introduce_score = 20
    music_cost = 3
    bot_user_name = "fa_cwc_bot"
    min_score_for_lottery = 100
    test_context_number = 100
    train_epochs = 1
    train_max_queue_length = 1000
    device = torch.device("cuda" if torch.cuda.is_available() and not DEBUG else "cpu")
    print(f"device: {device}")
