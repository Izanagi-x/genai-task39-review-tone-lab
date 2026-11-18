FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/home/user/.cache/huggingface \
    TOKENIZERS_PARALLELISM=false

RUN useradd -m -u 1000 user
WORKDIR /home/user/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=user:user . .
USER user
RUN python -c "from inference import load_model; load_model()"
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
