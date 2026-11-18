---
title: Review Tone Lab
emoji: 💬
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.32.0
python_version: "3.12"
app_file: hf_app.py
pinned: false
---

# Review Tone Lab

A small generative sentiment demo using the public
google/flan-t5-small model. Enter a short review and generate a positive or
negative label. No inference-provider API key is required.

The Streamlit Cloud deployment uses app.py. This free Hugging Face deployment
uses the Gradio interface in hf_app.py with the same inference.py model engine.
Docker was marked as paid and unavailable in the account's creation form, so the
free Gradio/ZeroGPU option was selected. Hugging Face inference uses a short
on-demand GPU handler; Streamlit Cloud and local tests use CPU inference.

The application uses the model's actual token generation, with a pinned model
revision. It supports short inputs and caches its model across requests.
Mixed opinions, sarcasm and ambiguous reviews can produce incorrect labels.

For local setup, both hosting workflows, validation and the platform comparison,
see [Readme.md](Readme.md).
