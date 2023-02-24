pip3 install -r requirements.txt && \
g++ -Wall -Wextra -Werror -pedantic -o kelp kelp.cpp && \
mkdir -p /usr/local/lib/command_helper && \
cp helper.py /usr/local/lib/command_helper/helper.py && \
cp config.json /usr/local/lib/command_helper/config.json && \
cp kelp /usr/local/bin/kelp && \
chmod +x /usr/local/bin/kelp