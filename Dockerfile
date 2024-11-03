FROM python:3.12-slim-bookworm

# install build tools
RUN apt update && apt install -y --no-install-recommends build-essential
# install os dependencies
RUN apt install -y --no-install-recommends libmariadb-dev

# upgrade pip
# install pip packages requiring os dependencies
RUN pip install --root-user-action ignore --upgrade pip && \
    pip install --root-user-action ignore --no-cache-dir mariadb

# clean os dependencies
RUN apt remove -y build-essential && apt clean -y && apt autoremove -y && rm -rf /var/lib/apt/lists/*

# create user
ARG USERNAME=python
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# switch user
USER ${USERNAME}
ENV PATH=${PATH}:/home/${USERNAME}/.local/bin

COPY . .
RUN pip install --user --no-cache-dir .[mariadb]

# configure run
WORKDIR /work
ENTRYPOINT ["chronovoyage"]
