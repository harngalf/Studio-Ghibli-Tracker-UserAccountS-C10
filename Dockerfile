FROM python:3.10.4

# 
WORKDIR /

# 
COPY ./requirements.txt /requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 
COPY ./app /

#
EXPOSE 3333

# 
CMD ["uvicorn", "app.main:app","--proxy-headers","--host", "0.0.0.0", "--port", "80"]
