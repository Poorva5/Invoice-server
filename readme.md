## Invoice project

## Steps to install locally

# create virtual env
```python
virtualenv venv
source venv/bin/activate
```

# install requirements
```python
python3 -m pip install -r requirements.txt
```

# migrate 
```python
python3 manage.py migrate
```

# create superuser
```python
python3 manage.py createsuperuser
```