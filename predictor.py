import torch
import string
from transformers import RobertaTokenizer, RobertaForMaskedLM

# Load pre-trained model and tokenizer
tokenizer = RobertaTokenizer.from_pretrained("roberta-large")
model = RobertaForMaskedLM.from_pretrained("roberta-large").eval()

TOP_K = 10  # Number of top predictions to consider


def decode_predictions(tokenizer, pred_indices, top_clean):
    """
    Decodes the top prediction indices into tokens, ignoring specified tokens.

    Args:
    tokenizer (RobertaTokenizer): The tokenizer used for decoding.
    pred_indices (list): List of predicted token indices.
    top_clean (int): Number of top tokens to return.

    Returns:
    list: List of decoded tokens.
    """
    ignore_tokens = string.punctuation + "[PAD]"
    tokens = [
        tokenizer.decode(idx).strip()
        for idx in pred_indices
        if tokenizer.decode(idx).strip() not in ignore_tokens
    ]
    return tokens[:top_clean]


def encode_input(tokenizer, text, add_special_tokens=True):
    """
    Encodes the input text into input IDs and finds the mask index.

    Args:
    tokenizer (RobertaTokenizer): The tokenizer used for encoding.
    text (str): The input text containing the <mask> token.
    add_special_tokens (bool): Whether to add special tokens.

    Returns:
    tuple: Input IDs tensor and mask index.
    """
    text = text.replace("<mask>", tokenizer.mask_token)
    if text.split()[-1] == tokenizer.mask_token:
        text += " ."

    input_ids = torch.tensor(
        [tokenizer.encode(text, add_special_tokens=add_special_tokens)]
    )
    mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].item()
    return input_ids, mask_idx


def get_top_predictions(text, top_clean=5):
    """
    Generates top predictions for the masked token in the input text.

    Args:
    text (str): The input text containing the <mask> token.
    top_clean (int): Number of top tokens to return.

    Returns:
    list: List of top predicted tokens.
    """
    input_ids, mask_idx = encode_input(tokenizer, text)
    with torch.no_grad():
        predictions = model(input_ids)[0]
    top_predictions = predictions[0, mask_idx, :].topk(TOP_K).indices.tolist()
    return decode_predictions(tokenizer, top_predictions, top_clean)
