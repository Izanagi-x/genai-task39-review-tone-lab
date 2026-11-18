# Assignment 39 - GenAI app deployment

Review Tone Lab is a Streamlit application that uses actual FLAN-T5 token
generation to classify a short review as positive or negative. It uses a pinned
public model revision, CPU inference on Streamlit Cloud and on-demand GPU inference
on Hugging Face, with no hosted-provider API key.

## Project files

- app.py: input, example buttons, generated-label display and session state.
- inference.py: cached resources are loaded by the UI; generation and input/token
  bounds are implemented here. The model is loaded without remote custom code.
- requirements.txt: pinned Python dependencies and the official CPU wheel index.
- hf_app.py: Gradio interface with a registered ZeroGPU handler.
- hf_space/requirements.txt: compatible dependencies for the active Space.
- Dockerfile: optional non-root Streamlit deployment recipe on port 8501;
  not used by the active Space.
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

The assignment's original Streamlit SDK has been deprecated. Docker is its
current replacement, but the signed-in account's creation form marks Docker as
paid/unavailable and disables CPU Basic. The available free Gradio/ZeroGPU option
was used instead. The Space uses hf_app.py as a Gradio interface over the same
inference.py engine, model revision, prompt and validation as the Streamlit app.
This is an explicit platform adaptation, not a claim that a Streamlit SDK Space
was created. The supplied Dockerfile remains an optional Streamlit deployment
recipe for an account with Docker access; it is not the active Space runtime.

1. Create a public Gradio Space using the available free hardware.
2. Upload README.md, hf_app.py, inference.py and Readme.md. Upload
   hf_space/requirements.txt as requirements.txt at the Space root. The free
   ZeroGPU runtime requires its supported torch==2.13.0; the Streamlit Cloud
   requirements retain the locally tested torch==2.15.0+cpu.
3. README.md pins sdk_version: 6.32.0, python_version: 3.12 and app_file: hf_app.py.
   The SDK installs Gradio; requirements.txt supplies the model dependencies.
4. Open the app and test both review examples and empty input. The public model
   is cached after its first load. The Space uses a 15-second on-demand @spaces.GPU handler. Its model is
   placed on CUDA during startup under the ZeroGPU emulator; the Streamlit
   deployment keeps CPU inference.

References: [Gradio Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-gradio),
[Streamlit Space migration](https://huggingface.co/docs/hub/main/spaces-sdks-streamlit).

## Task 3 - Platform comparison

| Area | Streamlit Community Cloud | Hugging Face Spaces |
| --- | --- | --- |
| Source workflow | Deploy a GitHub branch and app entrypoint | Use a Space repository; upload or push files |
| Environment in this project | Python version plus requirements.txt | Gradio SDK metadata plus requirements.txt; shared model engine |
| Strength | Simple workflow for a conventional Streamlit app | Managed model-demo interface and model ecosystem |
| Tradeoff | Less control over the underlying runtime | Free account required a Gradio interface adaptation |
| Good fit | Quick dashboards and small Streamlit tools | Gradio model demos; Docker is an alternative when available |

Both need reproducible dependencies, resource-aware models, working startup
commands and live verification. Cold starts include model loading, so the first
request can be slower than later requests. A successful build alone does not
prove that inference or input handling works. This assignment uses identical
inference code, weights and review inputs to compare the actual end-to-end behavior.

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
Both public deployments passed live positive, negative and empty-input checks.
The URLs and observed results are recorded in results/deployments.json.

A binary sentiment model can misread sarcasm, mixed opinions and unfamiliar
wording. Two successful examples validate the deployment path, not general
classification accuracy.

## Current deployment record

Verified on 18 November 2026:

- Source: https://github.com/Izanagi-x/genai-task39-review-tone-lab
- Streamlit Cloud: https://izanagi-review-tone-lab.streamlit.app/
- Hugging Face Space: https://huggingface.co/spaces/Ragnarith/review-tone-lab
- Direct Space app: https://ragnarith-review-tone-lab.hf.space/

Both live apps returned Positive / positive for “I loved this helpful book.”
and Negative / negative for “This was a terrible waste of time.” Empty input
showed “Enter a short review first.” The Streamlit result was also cleared after
empty input; Gradio displayed error indicators and the validation message.
Screenshots are included in results/.

Streamlit uses Python 3.12, Streamlit 1.67.0 and torch 2.15.0+cpu. The Space uses
Python 3.12, Gradio 6.32.0, spaces 0.52.1 and supported torch 2.13.0. Both use
transformers 5.23.0 and the same pinned model weights, prompt and input bounds.
The negative Space request briefly waited for an available GPU, then completed.
Free hardware quotas, cold starts and availability can affect future requests.

The Gradio interface also passed actual local positive/negative model calls and
empty-input rejection. Those results are in results/gradio_local_actual_results.json.
The Space is a Gradio/ZeroGPU adaptation because Docker and CPU Basic were
unavailable in this account's free creation form; it is not a Streamlit SDK Space.
