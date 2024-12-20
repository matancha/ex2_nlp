from transformers import RobertaTokenizerFast, RobertaModel
import torch
from sklearn.metrics.pairwise import cosine_similarity


tokenizer = RobertaTokenizerFast.from_pretrained("roberta-base")
model = RobertaModel.from_pretrained("roberta-base")

def calculate_word_embedding(sentence, target_word):
    inputs = tokenizer(sentence, return_tensors='pt', return_offsets_mapping=True)
    word_indices = [idx for idx, (start, end) in enumerate(inputs['offset_mapping'][0].tolist()) if sentence[start:end] == target_word]
    inputs = tokenizer(sentence, return_tensors='pt')

    with torch.no_grad():
        outputs = model(**inputs)

    hidden_states = outputs.last_hidden_state
    word_embeddings = hidden_states[0, word_indices, :]

    if word_embeddings.shape[0] > 1:
        word_embedding = word_embeddings.mean(dim=0)
    else:
        word_embedding = word_embeddings.squeeze(0)

    return word_embedding

def get_tokenized_words(sentence):
    inputs = tokenizer(sentence, return_tensors='pt', return_offsets_mapping=True)
    words = [sentence[start:end] for (start, end) in inputs['offset_mapping'][0].tolist()]
    return words

if __name__ == '__main__':
    # sentence1 = 'I got money from the bank'
    # sentence2 = 'I sat by the river bank'
    sentence1 = 'The bat bit the person'
    sentence2 = 'The linebacker hit the ball without a wooden bat'
    target_word = 'bat'

    print(get_tokenized_words(sentence1))
    print(get_tokenized_words(sentence2))

    vec1 = calculate_word_embedding(sentence1, target_word)
    vec2 = calculate_word_embedding(sentence2, target_word)
    print(cosine_similarity([vec1], [vec2]))


# from transformers import pipeline
# unmasker = pipeline('fill-mask', model='roberta-base')
# # sentence = 'I <mask> so sorry'
# input = '<s>' + sentence + '</s>'
# print(unmasker(input))