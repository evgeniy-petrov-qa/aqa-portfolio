# syntax=docker/dockerfile:1
FROM python:3.14-slim

# uv — project package manager (see CLAUDE.md / pyproject.toml)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy only dependency manifests first — this layer is cached by Docker
# and won't be rebuilt when test code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Now copy the rest of the project code
COPY . .

# Only chromium is needed (default browser in conftest.py).
# --with-deps installs the system libraries required by the headless browser.
RUN uv run playwright install --with-deps chromium

# Make the project's venv the container's default Python environment,
# so commands can run without the "uv run" prefix.
ENV PATH="/app/.venv/bin:$PATH"

# Default — fast smoke suite (headless chromium, env=test are the defaults in conftest.py).
# Run the full suite / a different env by overriding the command:
#   docker run --env-file .env <image> pytest -m regression
CMD ["pytest", "-m", "smoke"]