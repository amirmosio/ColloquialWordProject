import torch
from transformers import BertTokenizer, BertForMaskedLM, pipeline, AdamW


class BertLanguageModelService:
    model_pretrained_name = "HooshvareLab/bert-fa-zwnj-base"

    def __init__(self):
        # _config = AutoConfig.from_pretrained(self.model_pretrained_name)
        self._tokenizer = BertTokenizer.from_pretrained(self.model_pretrained_name)
        self._model = BertForMaskedLM.from_pretrained(self.model_pretrained_name)

        self._fill_mask = pipeline("fill-mask", model=self.model_pretrained_name, tokenizer=self._tokenizer)

    def _tokenize(self, formal_target):
        input_ids = self._tokenizer(
            formal_target,
            add_special_tokens=False,
            return_attention_mask=False,
            return_token_type_ids=False,
            max_length=1,
            truncation=True,
        )["input_ids"]

        if len(input_ids) == 0:
            return None
        id_ = input_ids[0]
        return self._tokenizer.convert_ids_to_tokens(id_)

    def get_prediction_score_with_fill_mask(self, sentence, word):
        return self._fill_mask(sentence, targets=[word])[0]["score"]

    def word_vector_in_context(self, sentence, idx):
        tok1 = self._tokenizer(sentence, return_tensors='pt')

        with torch.no_grad():
            out1 = self._model(**tok1)

        return out1.last_hidden_state[-1].squeeze()[[idx]]

    # def train_new_text(self, tokens):
    #     text = " ".join(tokens)
    #     inputs = self._tokenizer([text], return_tensors='pt', max_length=30, truncation=True, padding='max_length')
    #     inputs['labels'] = inputs.input_ids.detach().clone()
    #     rand = torch.rand(inputs.input_ids.shape)
    #     mask_arr = (rand < 0.15) * (inputs.input_ids != 101) * (inputs.input_ids != 102) * (inputs.input_ids != 0)
    #     selection = []
    #
    #     for i in range(inputs.input_ids.shape[0]):
    #         selection.append(
    #             torch.flatten(mask_arr[i].nonzero()).tolist()
    #         )
    #     for i in range(inputs.input_ids.shape[0]):
    #         inputs.input_ids[i, selection[i]] = 103
    #
    #     class TextDataset(torch.utils.data.Dataset):
    #         def __init__(self, encodings):
    #             self.encodings = encodings
    #
    #         def __getitem__(self, idx):
    #             return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
    #
    #         def __len__(self):
    #             return len(self.encodings.input_ids)
    #
    #     dataset = TextDataset(inputs)
    #     loader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)
    #     self._model.train()
    #     optim = AdamW(self._model.parameters(), lr=5e-5)
    #     for batch in loader:
    #         optim.zero_grad()
    #         input_ids = batch['input_ids']
    #         attention_mask = batch['attention_mask']
    #         labels = batch['labels']
    #         # process
    #         outputs = self._model(input_ids, attention_mask=attention_mask, labels=labels)
    #         loss = outputs.loss
    #         loss.backward()
    #         optim.step()
    #     self._model.eval()
    def save_model(self):
        pass

#
# if __name__ == '__main__':
#     model_service = BertLanguageModelService()
#     print("")
