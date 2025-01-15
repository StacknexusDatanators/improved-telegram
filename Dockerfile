# Use the official Miniconda image as a base
# Use the official Miniconda image as a base
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install GCC compiler
RUN apt-get update && apt-get install -y gcc && apt-get install -y build-essential cmake

# Set environment variables for ARM architecture
ENV CFLAGS="-march=armv8-a"
ENV CXXFLAGS="-march=armv8-a"

# Create a new conda environment with Python 3.9
RUN conda create -n myenv python=3.9

# Activate the environment and install dependencies
RUN /bin/bash -c "source activate myenv && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install streamlit"

CMD streamlit run streamlit_chat.py