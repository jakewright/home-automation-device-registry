FROM python:3.5.1-onbuild

# Upgrade pip
RUN pip install --upgrade pip

# Copy the application files
COPY . /usr/src/app/

# Set the working directory to where the application files are
WORKDIR /usr/src/app