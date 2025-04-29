FROM python@sha256:c4c4ded064fdc28eab54fe119a0778c8a7915fc5b713497ff4cc5fdcab0dacaa


# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install torch for CPU
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 10000

# Start the FastAPI app
CMD ["uvicorn", "myFastAPI.main:app", "--host", "0.0.0.0", "--port", "10000"]
