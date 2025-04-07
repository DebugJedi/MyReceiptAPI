FROM python:3.11

#Install system dependencies and Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Debug print
RUN echo "==> Checking Tesseract path manually..." && \
    find / -name tesseract && \
    which tesseract && \
    tesseract --version


RUN which tesseract && tesseract --version

# Set the working directory
WORKDIR /app

RUN which tesseract

RUN echo "✅ Tesseract Path: $(which tesseract)"

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port app will run on
EXPOSE 10000

# Command to run the application
CMD [ "uvicorn", "myFastAPI.main:app", "--host", "0.0.0.0", "--port", "10000" ]
