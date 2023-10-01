# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /be

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /be/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy app folder to docker
COPY ./app /be/app

# Run app.py when the container launches
CMD ["python", "app.py"]