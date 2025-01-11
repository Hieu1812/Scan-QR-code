FROM python:3.9
COPY *.py setup.cfg LICENSE README.md requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN python main.py