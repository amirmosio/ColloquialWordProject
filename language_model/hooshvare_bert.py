import numpy as np
import torch
from transformers import AutoConfig, BertTokenizerFast, BertModel, pipeline

model_name_or_path = "HooshvareLab/bert-fa-zwnj-base"
config = AutoConfig.from_pretrained(model_name_or_path)
tokenizer = BertTokenizerFast.from_pretrained(model_name_or_path)
model = BertModel.from_pretrained(model_name_or_path)

fill_mask = pipeline("fill-mask", model=model_name_or_path, tokenizer=tokenizer)


def word_vector_in_context(sentence, idx):
    tok1 = tokenizer(sentence, return_tensors='pt')

    with torch.no_grad():
        out1 = model(**tok1)

    return out1.last_hidden_state[-1].squeeze()[[idx]]
