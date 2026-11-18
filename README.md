---
title: Review Tone Lab
emoji: 💬
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
---

# Review Tone Lab

A small generative sentiment demo built with Streamlit and the public
google/flan-t5-small model. Enter a short review and generate a positive or
negative label. No inference-provider API key is required.

The application uses the model's actual token generation, with a pinned model
revision. It supports short inputs and caches its model across requests.
Mixed opinions, sarcasm and ambiguous reviews can produce incorrect labels.

For local setup, both hosting workflows, validation and the platform comparison,
see [Readme.md](Readme.md).
