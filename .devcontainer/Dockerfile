ARG VARIANT
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

# Dependencias + uv instalado de forma global
RUN apt-get update && apt-get install -y --no-install-recommends \
    git jq bash-completion make ripgrep curl ca-certificates  \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    # mueve/instala uv y uvx al PATH global para TODOS los usuarios
    && install -m 0755 /root/.local/bin/uv  /usr/local/bin/uv \
    && install -m 0755 /root/.local/bin/uvx /usr/local/bin/uvx


RUN curl -1sLf 'https://dl.cloudsmith.io/public/task/task/setup.deb.sh' | bash \
    && apt-get update && apt-get install -y --no-install-recommends task 


# (opcional) autocompletado bash
RUN echo 'if [ -f /etc/bash_completion ]; then . /etc/bash_completion; fi' >> /etc/bash.bashrc