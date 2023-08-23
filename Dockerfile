FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

CMD ["python", "index.py"]

ENV TOKEN=""

ENTRYPOINT ["sh", "-c", "sed -i \"s/\\\"token\\\": \\\".*\\\"/\\\"token\\\": \\\"$TOKEN\\\"/\" data.json && python index.py"]