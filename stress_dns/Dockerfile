# Use Python base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /stress_dns

# Copy the Python script into the container
COPY stress_dns.py .

# Define environment variables for configuration
ENV TARGET_HOST ""
ENV DNS_SERVER ""
ENV NUM_REQUESTS 100
ENV NUM_THREADS 10

# Run stress_dns
CMD ["python", "stress_dns.py"]