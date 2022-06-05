from hooshvare_bert import fill_mask, model, tokenizer, word_vector_in_context

if __name__ == '__main__':

    embedding = model(**tokenizer("داداش", return_tensors="pt")).pooler_output
    print(embedding)

    examples = [
        "سلام بر [MASK]",
    ]
    for example in examples:
        for prediction in fill_mask(example, targets=["دوستان"]):
            print(f"{prediction['sequence']}, confidence: {prediction['score']}")
        print("=" * 50)

    res = word_vector_in_context("سلام بر دوستان", 2)
    print(res)
