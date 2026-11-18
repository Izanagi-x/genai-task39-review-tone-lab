"""Boundary/normalization fixtures; actual model outputs are recorded by demo.py."""
import threading
import torch
from inference import classify_review

class TokenizerFixture:
    def __init__(self, response='positive', length=10):
        self.response, self.length = response, length
    def __call__(self, text, **kwargs):
        assert 'Classify the sentiment' in text and kwargs['truncation'] is False
        return {'input_ids': torch.ones((1, self.length), dtype=torch.long)}
    def decode(self, ids, **kwargs):
        assert kwargs['skip_special_tokens'] is True
        return self.response

class ModelFixture:
    def __init__(self): self.calls = 0
    def generate(self, **kwargs):
        assert kwargs['max_new_tokens'] == 8 and kwargs['do_sample'] is False
        self.calls += 1
        return torch.tensor([[1]])

if __name__ == '__main__':
    for generated, expected in [('positive', 'Positive'), ('Negative.', 'Negative'), ('uncertain', 'Unclear')]:
        model = ModelFixture()
        result = classify_review('A short review.', (TokenizerFixture(generated), model, threading.Lock()))
        assert result['label'] == expected and result['generated_text'] == generated
        assert model.calls == 1
    model = ModelFixture()
    for value in ['', '  ', None, 3, 'x' * 801]:
        try: classify_review(value, (TokenizerFixture(), model, threading.Lock()))
        except ValueError: pass
        else: raise AssertionError('Invalid review accepted')
    try: classify_review('review', (TokenizerFixture(length=257), model, threading.Lock()))
    except ValueError: pass
    else: raise AssertionError('Oversized token sequence accepted')
    assert model.calls == 0
    print('Input/token limits, deterministic generation options and positive/negative/unexpected-label handling passed with explicit fixtures.')
