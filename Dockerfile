# 1. Start with a tiny, fast version of Linux that has 'mamba' installed
FROM mambaorg/micromamba:latest

# 2. Copy your tool list (env.yaml) into the container's temporary folder
COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml

# 3. Tell mamba to install all the bioinformatics tools from that file
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

# 4. Set the internal "working directory" where your code will live
WORKDIR /app

# 5. Copy all your project files from your computer into the container
COPY . /app

# 6. Set the command that runs automatically when the container starts
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "-m", "rnaseq_pipeline"]

# 7. If the user doesn't provide arguments, show the "help" menu by default
CMD ["--help"]