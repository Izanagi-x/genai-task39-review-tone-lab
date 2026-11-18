"""Free Gradio Space interface using the same model engine as the Streamlit app."""
import spaces
import os
from functools import lru_cache
import gradio as gr
from inference import load_model, classify_review

DEVICE = 'cuda' if os.environ.get('SPACE_ID') else 'cpu'

@lru_cache(maxsize=1)
def resources():
    return load_model(device=DEVICE)

# ZeroGPU requires CUDA placement during startup; its emulator makes this safe
# before a real GPU is allocated. Local execution keeps the CPU path.
resources()

@spaces.GPU(duration=15)
def gpu_generate(review):
    return classify_review(review, resources(), device=DEVICE)

def generate_label(review):
    try:
        if not isinstance(review, str) or not review.strip():
            raise ValueError('Enter a short review first.')
        if len(review.strip()) > 800:
            raise ValueError('Keep the review to 800 characters or fewer.')
        result = gpu_generate(review)
        return result['label'], result['generated_text']
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc
    except Exception as exc:
        raise gr.Error('The model could not finish this request. Please try again.') from exc

with gr.Blocks(title='Review Tone Lab') as demo:
    gr.Markdown('# Review Tone Lab\nExplore how a generative language model reads the tone of a short review.')
    review = gr.Textbox(label='Your review', value='I loved this helpful book.', lines=4, max_lines=8)
    gr.Examples(examples=[['I loved this helpful book.'], ['This was a terrible waste of time.']], inputs=review)
    button = gr.Button('Generate label', variant='primary')
    tone = gr.Textbox(label='Generated tone', interactive=False)
    raw = gr.Textbox(label='Model output', interactive=False)
    button.click(generate_label, inputs=review, outputs=[tone, raw])
    gr.Markdown('A small-model demonstration for short reviews. Mixed or ambiguous opinions can be difficult to classify.')

if __name__ == '__main__':
    demo.queue().launch(server_name='0.0.0.0', server_port=7860, show_error=False)
