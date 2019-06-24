FROM python:3-alpine
RUN python3 -m pip install docker
COPY directory.py /directory.py
EXPOSE 80
CMD ["/usr/local/bin/python3", "/directory.py"]
