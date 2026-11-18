"""Actual model calls used for local and deployed-app comparison."""
from pathlib import Path
import json
from inference import load_model, classify_review

if __name__ == '__main__':
    resources = load_model()
    rows = []
    for review, expected in [('I loved this helpful book.', 'Positive'),
                             ('This was a terrible waste of time.', 'Negative')]:
        result = classify_review(review, resources)
        rows.append({**result, 'expected_for_validation': expected})
        print(json.dumps(rows[-1]), flush=True)
        assert result['label'] == expected, rows[-1]
    root = Path(__file__).resolve().parent
    (root / 'results').mkdir(exist_ok=True)
    (root / 'results/local_actual_results.json').write_text(json.dumps({
        'execution': 'actual local Transformers model.generate calls', 'results': rows}, indent=2))
