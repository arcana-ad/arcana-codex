# Codex: Python SDK for Arcana

The Arcana Codex Python library provides convenient access to the Arcana Gateway Ad Service from any Python 3.10+ applications. The library includes type definitions for all request params and response fields, and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Installation

```sh
# install from PyPI
pip install arcana-codex
```

## Usage

```python
import os
from arcana_codex import ArcanaCodexClient, AdUnitsFetchModel, AdUnitsIntegrateModel

client = ArcanaCodexClient(
    api_key=os.environ.get("ARCANA_CODEX_API_KEY"),
)

fetch_payload = AdUnitsFetchModel(query="How can I write blogs for my website?")
fetch_result = sync_fetch_version(client, fetch_payload)

ad_unit_ids = [ad_unit["id"] for ad_unit in fetch_result["response_data"]]


integrate_payload = AdUnitsIntegrateModel(
    ad_unit_ids=ad_unit_ids, base_content="insert the llm response generated from your application as the base content"
)
integration_result = sync_fetch_version(client, integrate_payload)

print(integration_result)
```

While you can provide an `api_key` keyword argument, we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/) (or something similar) to add `ARCANA_CODEX_API_KEY="My Arc API Key"` to your `.env` file so that your API Key is not stored in source control.