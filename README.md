# filigree

<div align="center">

[![Build status](https://github.com/daisie-lab/filigree/workflows/build/badge.svg?branch=master&event=push)](https://github.com/daisie-lab/filigree/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/filigree.svg)](https://pypi.org/project/filigree/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/daisie-lab/filigree/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/charliermarsh/ruff)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/daisie-lab/filigree/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/daisie-lab/filigree/releases)
[![License](https://img.shields.io/github/license/daisie-lab/filigree)](https://github.com/daisie-lab/filigree/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

`filigree` is a Python cli/package

</div>

## Very first steps

### Initialize your code

1. Initialize `git` inside your repo:

```bash
cd filigree && git init
```

2. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

3. Initialize poetry and install `pre-commit` hooks:

```bash
make install
make pre-commit-install
```

4. Run the codestyle:

```bash
make codestyle
```

5. Upload initial code to GitHub:

```bash
git add .
git commit -m ":tada: Initial commit"
git branch -M main
git remote add origin https://github.com/daisie-lab/filigree.git
git push -u origin main
```

### Provide your API keys

Provide API keys following the template below as a ```.env``` file.
```bash
DEEPGRAM_API_KEY=
OPENAI_API_KEY=
```

### Update Personas

Update AI Personas to analyze the transcription in ```filigree/personas.py```

### Run Example

```bash
streamlit run filigree/main.py
```