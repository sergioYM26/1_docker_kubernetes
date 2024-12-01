FROM python:3.11

# Update work directory (like cd linux command)
WORKDIR /app/

# Install dependencies BEFPORE copying code, optimize cache usage
RUN pip install flask sqlalchemy Flask-SQLAlchemy psycopg2-binary

# Environment variables with default values
ENV DB_USER=testuser
ENV DB_PASSWORD=testpass
ENV DB_HOST=db-docker
ENV DB_PORT=5432
ENV DB_NAME=datahack
ENV VERSION=0.0.0-SYM

# Copy code AFTER installing dependencies, optimize cache usage
COPY myapp.py .

# This is only info, does nothing
EXPOSE 5000

# Arguments to entrypoint
CMD [ "python", "myapp.py" ]