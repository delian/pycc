FROM mcr.microsoft.com/devcontainers/base:noble

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install git zsh tmux vim python3 python-is-python3 python3-poetry \
    llvm clang make tmux fish

USER vscode
WORKDIR /workspace

CMD ["/bin/zsh"]

