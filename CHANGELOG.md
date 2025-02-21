# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PyPA Versioning Specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers).

## v0.1.0 - [Unreleased]
### Added
- Implemented `AsyncArcanaCodexClient` and `ArcanaCodexClient` for interacting with the Arcana Forge API.
    - Added `_internals.py` to handle HTTP response codes and exceptions (including `BadRequestException`, `UnauthorizedException`, `ForbiddenException`, `NotFoundException`, `UnprocessableEntityException`, `RateLimitException`, `InternalServerErrorException`, and a generic `APIException`).
    - Added `_utils.py` with a `Result` class using Pydantic for handling responses with either a value or an error.
    - Added `models.py` with `AdUnitsFetchModel` for fetching ad units based on query and `AdUnitsIntegrateModel` for integrating ad units with base content.
    - Added `exceptions.py` to define custom exceptions for API interactions.
    - Added `client.py` and `async_client.py` with `fetch_ad_units` and `integrate_ad_units`.
- Added configuration for GitHub Issue templates (`.github/ISSUE_TEMPLATE/config.yml`). Disables blank issues and directs users to the Arcana Community discussions.
- Added timeout to httpx requests.
- Added error raising for non-successful responses.

----------------------------------------------------------------