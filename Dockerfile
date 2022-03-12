# #For more information, please refer to https://aka.ms/vscode-docker-python
# FROM public.ecr.aws/lambda/python:3.8

# # Copy function code
# COPY etl-sel.py ${LAMBDA_TASK_ROOT}
# # Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

# # Install pip requirements
# COPY requirements.txt .
# RUN python -m pip install -r requirements.txt

# RUN mkdir driver
# COPY driver/chromedriver /usr/bin/chromedriver


# RUN chmod 755 /usr/bin/chromedriver


# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["etl-sel.scraper"]

   
FROM public.ecr.aws/lambda/python@sha256:258a25364fd462f6c6c387cf1bea4a79fa1a8b09aee578aef2c7c50b5efca928 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/99.0.4844.51/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F961656%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:258a25364fd462f6c6c387cf1bea4a79fa1a8b09aee578aef2c7c50b5efca928
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/
COPY etl-sel.py ./
CMD [ "etl-sel.scraper" ]