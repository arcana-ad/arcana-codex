# Codex: Python SDK for Atheon

The Atheon Codex Python library provides convenient access to the Atheon Gateway Ad Service from any Python 3.10+ applications. The library includes type definitions for all request params and response fields, and offers both synchronous and asynchronous clients powered by [httpx](https://github.com/encode/httpx).

## Installation

```sh
# install from PyPI
pip install atheon-codex
```

## Usage

```python
import os
from atheon_codex import AtheonCodexClient, AdUnitsFetchModel, AdUnitsIntegrateModel

client = AtheonCodexClient(
    api_key=os.environ.get("ATHEON_CODEX_API_KEY"),
)

fetch_payload = AdUnitsFetchModel(query="How can I write blogs for my website?")
fetch_result = client.fetch_ad_units(fetch_payload)

ad_unit_ids = [ad_unit["id"] for ad_unit in fetch_result["response_data"]]


integrate_payload = AdUnitsIntegrateModel(
    ad_unit_ids=ad_unit_ids, base_content="insert the llm response generated from your application as the base content"
)
integration_result = client.fetch_ad_units(integrate_payload)

print(integration_result)
```

While you can provide an `api_key` keyword argument, we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/) (or something similar) to add `ATHEON_CODEX_API_KEY="My Eon API Key"` to your `.env` file so that your API Key is not stored in source control.