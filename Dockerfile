# Specify Base Container
FROM python:3.9

# Copy our files
COPY ./ /code

# Ensure we're starting in the correct folder
WORKDIR /code

# Install python libraries
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the Rest API
CMD ["uvicorn", "WeatherRestAPI:app", "--host", "0.0.0.0", "--port", "80"]