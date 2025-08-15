FROM python:3.9-slim
WORKDIR /app
COPY order-service.py .
RUN pip install flask requests
CMD ["python", "order-service.py"]