"""Checking Embeddings similarities for the same word"""

from typing import TypedDict, cast

from torch.nn.functional import cosine_similarity
from torchtyping import TensorType
from transformers import AutoModel, AutoTokenizer
from transformers.modeling_outputs import BaseModelOutputWithPoolingAndCrossAttentions
from transformers.tokenization_utils_base import BatchEncoding


class EmbeddingsReturnType(TypedDict):
    """thing"""

    tokens: BatchEncoding
    embeddings: BaseModelOutputWithPoolingAndCrossAttentions


class VizEmbeddings:
    """class to visualize embeddings for a given word"""

    def __init__(self) -> None:
        self.tokenizer: AutoTokenizer = self.get_tokenizer()
        self.model: AutoModel = self.get_model()

    def get_tokenizer(
        self,
        path: str = "google-bert/bert-base-uncased",
    ) -> AutoTokenizer:
        """Get the Tokenizer"""
        return cast(AutoTokenizer, AutoTokenizer.from_pretrained(path))

    def get_model(
        self,
        path: str = "google-bert/bert-base-uncased",
    ) -> AutoModel:
        """Get the Model"""
        return cast(AutoModel, AutoModel.from_pretrained(path))

    def get_embeddings(
        self,
        document: str,
    ) -> EmbeddingsReturnType:
        """Get embeddings"""
        tokens: BatchEncoding = self.tokenizer(document, return_tensors="pt")
        embeddings: BaseModelOutputWithPoolingAndCrossAttentions = self.model(**tokens)
        return {"tokens": tokens, "embeddings": embeddings}

    def get_tokens(
        self,
        document: str,
    ) -> list[str]:
        """Get Tokens"""
        tokens: list[str] = self.tokenizer.tokenize(document)
        return tokens

    def find_token_indices(
        self,
        token_ids: BatchEncoding,
        target_token_id: int,
    ) -> list[int]:
        """Thing"""
        token_list: list[int] = token_ids.input_ids[0].tolist()
        return [id for id, token in enumerate(token_list) if token == target_token_id]

    def get_token_embedding(
        self,
        embedding: BaseModelOutputWithPoolingAndCrossAttentions,
        token_idx: int,
    ) -> TensorType[768]:
        """Thing."""
        # Filter to get the embedding of our token_id
        squeezed_embeddings: TensorType[768, 13] = embedding.last_hidden_state.squeeze()
        return squeezed_embeddings[token_idx]


SENTENCE_1 = "I'm going to the bank to deposit money."
SENTENCE_2 = "I'm going to wait by the river bank."
SENTENCE_3 = "I'm going to wait by the bank after withdrawing money"

v = VizEmbeddings()


embeddings_return_1 = v.get_embeddings(SENTENCE_1)
tokens_1: BatchEncoding = embeddings_return_1["tokens"]

# Pooler output is the classification task for the whole doc
# Last hidden state is the embedding per token of the doc
embeddings_1: BaseModelOutputWithPoolingAndCrossAttentions = embeddings_return_1["embeddings"]

embeddings_return_2 = v.get_embeddings(SENTENCE_2)
tokens_2: BatchEncoding = embeddings_return_2["tokens"]
embeddings_2: BaseModelOutputWithPoolingAndCrossAttentions = embeddings_return_2["embeddings"]

embeddings_return_3 = v.get_embeddings(SENTENCE_3)
tokens_3: BatchEncoding = embeddings_return_3["tokens"]
embeddings_3: BaseModelOutputWithPoolingAndCrossAttentions = embeddings_return_3["embeddings"]


bank_token_info: BatchEncoding = v.tokenizer("bank", add_special_tokens=False)
bank_token_id: int = bank_token_info.input_ids[0]

bank_indices_1: list[int] = v.find_token_indices(tokens_1, bank_token_id)
bank_indices_2: list[int] = v.find_token_indices(tokens_2, bank_token_id)
bank_indices_3: list[int] = v.find_token_indices(tokens_3, bank_token_id)

bank_embeddings: list[int | None] = []
bank_embeddings_1: TensorType[768] = v.get_token_embedding(embeddings_1, bank_indices_1[0])
bank_embeddings_2: TensorType[768] = v.get_token_embedding(embeddings_2, bank_indices_2[0])
bank_embeddings_3: TensorType[768] = v.get_token_embedding(embeddings_3, bank_indices_3[0])

sim_12: TensorType[1] = cosine_similarity(bank_embeddings_1, bank_embeddings_2, dim=0)
sim_13: TensorType[1] = cosine_similarity(bank_embeddings_1, bank_embeddings_3, dim=0)
sim_23: TensorType[1] = cosine_similarity(bank_embeddings_2, bank_embeddings_3, dim=0)

print(f"{sim_12.item()=}")
print(f"{sim_13.item()=}")
print(f"{sim_23.item()=}")
