FROM python:3.11




# Set the working directory
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port app will run on
EXPOSE 10000

# Command to run the application
CMD [ "uvicorn", "myFastAPI.main:app", "--host", "0.0.0.0", "--port", "10000" ]
