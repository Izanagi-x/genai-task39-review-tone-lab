from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def classify_fixture(review, resources):
    return {'review': review, 'label': 'Negative' if 'terrible' in review else 'Positive',
            'generated_text': 'explicit offline UI fixture', 'seconds': 0.1}

with (patch('inference.load_model', return_value=object()),
      patch('inference.classify_review', side_effect=classify_fixture)):
    app = AppTest.from_file(str(ROOT / 'app.py')).run()
    assert not app.exception
    next(b for b in app.button if b.label == 'Generate label').click().run()
    assert not app.exception and app.success[0].value == 'Positive'
    next(b for b in app.button if b.label == 'Negative example').click().run()
    assert not app.success and not app.info
    next(b for b in app.button if b.label == 'Generate label').click().run()
    assert not app.exception and app.info[0].value == 'Negative'
    app.text_area[0].set_value('').run()
    next(b for b in app.button if b.label == 'Generate label').click().run()
    assert not app.exception and app.error and not app.info
print('Streamlit examples, generated-label display, stale-result clearing and empty-input errors passed using explicit UI fixtures.')
