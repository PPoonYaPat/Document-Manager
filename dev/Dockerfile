FROM python:3.12-slim

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y neovim git less curl wget build-essential python3-dev

# Set git autocompletion & set safe directory & set bashrc
RUN echo "source /usr/share/bash-completion/completions/git" >>~/.bashrc && \
    git config --global --add safe.directory /workspace && \
    cat <<'EOF' >>~/.bashrc
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt
EOF

# Install uv for python package management
RUN wget -qO- https://astral.sh/uv/install.sh | sh && \
    source "${HOME}/.local/bin/env" && \
    uv venv "${HOME}/.venv" --python python3.12 && \
    source ${HOME}/.venv/bin/activate && uv pip install pip && \
    cat <<'EOF' >>~/.bashrc
if [ -z "$VIRTUAL_ENV" ]; then
    source ${HOME}/.venv/bin/activate
fi
EOF

WORKDIR /doc-manager