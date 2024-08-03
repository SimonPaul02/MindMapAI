FROM unit:1.32.1-python3.11
# Move the frontend executables to the www directory

# Build virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./backend/app/requirements.txt /opt/requirements.txt
# Install the required python packages
RUN pip install --no-cache-dir -r /opt/requirements.txt

# Copy the unit configuration files
COPY ./*.json /docker-entrypoint.d/
COPY ./frontend/dist /frontend
COPY ./backend/app /app

EXPOSE 8062
EXPOSE 8061