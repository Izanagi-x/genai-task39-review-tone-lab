"""Generate a binary review-sentiment label with a small public T5 model."""
import threading
import time

MODEL_ID = 'google/flan-t5-small'
REVISION = '0fc9ddf78a1e988dac52e2dac162b0ede4fd74ab'


def load_model():
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    torch.set_num_threads(2)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION,
                                              token=False, trust_remote_code=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, revision=REVISION,
        token=False, trust_remote_code=False, use_safetensors=True)
    model.eval()
    return tokenizer, model, threading.Lock()


def classify_review(review, resources):
    if not isinstance(review, str) or not review.strip():
        raise ValueError('Enter a short review first.')
    review = review.strip()
    if len(review) > 800:
        raise ValueError('Keep the review to 800 characters or fewer.')
    tokenizer, model, lock = resources
    prompt = 'Classify the sentiment as positive or negative: ' + review
    inputs = tokenizer(prompt, return_tensors='pt', truncation=False)
    if inputs['input_ids'].shape[-1] > 256:
        raise ValueError('Use a shorter review so the full text fits the model.')
    import torch
    started = time.monotonic()
    with lock, torch.inference_mode():
        outputs = model.generate(**inputs, max_new_tokens=8, do_sample=False, num_beams=1)
    raw = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    normalized = raw.lower().strip(' .!\n')
    label = normalized.capitalize() if normalized in ('positive', 'negative') else 'Unclear'
    return {'review': review, 'label': label, 'generated_text': raw,
            'model': MODEL_ID, 'revision': REVISION,
            'seconds': round(time.monotonic() - started, 3)}
