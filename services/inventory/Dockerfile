FROM python:3.9-slim
WORKDIR /app
COPY inventory-service.py .
RUN pip install flask
CMD ["python", "inventory-service.py"]