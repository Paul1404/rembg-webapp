# Use an intermediate image to download the model file
FROM alpine:latest as downloader

RUN apk --no-cache add curl

WORKDIR /model

# Download u2net.onnx model from GitHub releases
RUN curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o u2net.onnx

# Now, build the actual image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file, to cache the installed dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the downloaded model from the downloader stage
COPY --from=downloader /model/u2net.onnx /home/.u2net/u2net.onnx

# Copy the rest of the application
COPY . .

# Make port 5100 available to the world outside this container
EXPOSE 5100

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
