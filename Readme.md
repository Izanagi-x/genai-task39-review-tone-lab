# Assignment 39 - GenAI app deployment

Review Tone Lab is a Streamlit application that uses actual FLAN-T5 token
generation to classify a short review as positive or negative. It uses a pinned
public model revision and CPU inference, with no hosted-provider API key.

## Project files

- app.py: input, example buttons, generated-label display and session state.
- inference.py: cached resources are loaded by the UI; generation and input/token
  bounds are implemented here. The model is loaded without remote custom code.
- requirements.txt: pinned Python dependencies and the official CPU wheel index.
- Dockerfile: non-root Hugging Face deployment, model caching during the build,
  Streamlit server listening on port 8501.
- README.md: Hugging Face Space metadata and public app description.
- demo.py: actual-model smoke checks for the same two reviews used on both sites.
- results/: actual local model outputs and deployment verification evidence.

The model's original page is [google/flan-t5-small](https://huggingface.co/google/flan-t5-small).
The selected revision is pinned in inference.py so both deployments use the same
weights and tokenizer. Model weights, private credentials and virtual
environments are excluded from the submission ZIP and source repository.

## Local run

Use Python 3.12, matching both deployment environments.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The first local request downloads the public model; later requests reuse the
cache. Inputs are limited to 800 characters and 256 model input tokens, and
outputs to 8 generated tokens. Unexpected output is displayed as Unclear rather
than silently turned into a positive or negative label. A shared model lock
serializes concurrent inference, while results stay in each browser session.

## Task 1 - Streamlit Community Cloud

1. Push this project's files to a GitHub repository. Keep app.py and
   requirements.txt at the repository root.
2. Open your workspace at share.streamlit.io and select Create app, then the
   option for an existing app/repository.
3. Choose the repository, main branch and app.py entrypoint. Set Python 3.12 in
   Advanced settings. This app needs no secrets.
4. Deploy, watch the build logs and open the assigned streamlit.app URL.
5. Test the positive example, negative example and empty input. Record the live
   URL, deployment result and screenshots in results/.

References: [deploy an app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy),
[app dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies).

## Task 2 - Hugging Face Spaces

The original assignment calls this a Streamlit-type Space. That built-in SDK was
deprecated; the current supported workflow is a Docker Space running Streamlit.
The README.md YAML therefore sets sdk: docker and app_port: 8501.

1. Create a new Space in your own Hugging Face account, using the Docker SDK and
   basic CPU hardware. Use the Streamlit Docker template or the supplied files.
2. Upload the project files or push them to the Space's Git repository. The
   README.md, Dockerfile, requirements.txt, app.py and inference.py are required.
3. Watch the build. The Dockerfile downloads the pinned public model at build
   time as a non-root user, so its cache is readable and writable at runtime.
4. Open the live app and repeat the same positive, negative and empty-input
   checks. Record its Space URL, direct app URL, status and screenshots.

References: [current Streamlit Space guidance](https://huggingface.co/docs/hub/main/spaces-sdks-streamlit),
[Docker Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-docker).

## Task 3 - Platform comparison

| Area | Streamlit Community Cloud | Hugging Face Spaces |
| --- | --- | --- |
| Source workflow | Deploy a GitHub branch and app entrypoint | Use a Space repository; upload or push files |
| Environment in this project | Python version plus requirements.txt | Dockerfile controls the Python image, dependencies and startup |
| Strength | Simple workflow for a conventional Streamlit app | Flexible container setup and model-demo ecosystem |
| Tradeoff | Less control over the underlying runtime | More build/runtime configuration to maintain |
| Good fit | Quick dashboards and small Streamlit tools | Model demos or apps needing a custom container |

Both need reproducible dependencies, resource-aware models, working startup
commands and live verification. Cold starts include model loading, so the first
request can be slower than later requests. A successful build alone does not
prove that inference or input handling works. This assignment uses identical
code, weights and review inputs to compare the actual end-to-end behavior.

## Verification

```sh
python demo.py
python test_inference.py
python test_app.py
```

The actual local model produced positive for 'I loved this helpful book.' and
negative for 'This was a terrible waste of time.' These original outputs are in
results/local_actual_results.json. Explicit fixtures separately test bounds,
unexpected labels, example controls, state reset and empty-input handling.
Live deployment URLs and observed results belong in results/deployments.json
once each deployment is verified; pending deployments are not claimed as live.

A binary sentiment model can misread sarcasm, mixed opinions and unfamiliar
wording. Two successful examples validate the deployment path, not general
classification accuracy.

## Current deployment record

Published source: https://github.com/Izanagi-x/genai-task39-review-tone-lab

The app passes actual local inference and local UI checks. Streamlit Cloud and
Hugging Face live deployments are pending account sign-in; no live URL is
claimed yet. The final submission archive will be updated with both verified
live URLs and screenshots after deployment.
