# Beer Explorer Backend

## Description
This backend provides a RESTful API through Django Rest Framework.

## Current state
The backend provides a basic RESTful API to create, modify and delete beers and beer checkins. 
Due to a deadline to be live on the 1st of January, the focus was on getting the functionality ready. Over the coming period, code quality will be improved.

## Setup

Create .env file in the root of the project and add the following variables:
```python
DB_ENGINE=django.db.backends.postgresql
DB_SCHEMA=schema_name
DB_NAME=db_name
DB_USER=user
DB_PASSWORD=password
DB_HOST=host
DB_PORT=port
```

### Database operations

#### Permissions

Create a user for django and give the following permissions.

```
CREATE USER username with PASSWORD 'password';
GRANT ALL ON ALL TABLES IN SCHEMA public to username;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to username;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to username;
GRANT CREATE ON SCHEMA public TO username;
```

Create a superuser

```
python .\manage.py createsuperuser
```
