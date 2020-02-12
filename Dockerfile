FROM holbertonschool/ubuntu-1604-python35

CMD ["bash"]

WORKDIR /ChatLearner

RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
RUN apt-get install -y vim 
RUN apt-get install -y git
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

RUN pip3 install tensorflow==1.4.0
COPY . .
RUN pip3 install nltk
RUN python3 setnltk.py


# RUN bash settingpath.sh
ENV PYTHONPATH "${PYTHONPATH}:/ChatLearner"

RUN python3 settings.py
RUN pip install "numpy<1.17"

RUN npm install

EXPOSE 80
ENTRYPOINT node app.js

#RUN botbui.py
