# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PyPA Versioning Specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers).

## v0.1.0 - [Unreleased]
### Added
- Implemented `AsyncArcanaCodexClient` and `ArcanaCodexClient` for interacting with the Arcana Forge API.
    - Added `_internals.py` to handle HTTP response codes and exceptions (including `BadRequestException`, `UnauthorizedException`, `ForbiddenException`, `NotFoundException`, `UnprocessableEntityException`, `RateLimitException`, `InternalServerErrorException`, and a generic `APIException`).
    - Added `_utils.py` with a `Result` class using Pydantic for handling responses with either a value or an error.
    - Added `models.py` with `AdUnitsFetchModel` for request payload validation.
    - Added `exceptions.py` to define custom exceptions for API interactions.
- Added configuration for GitHub Issue templates (`.github/ISSUE_TEMPLATE/config.yml`).  Disables blank issues and directs users to the Arcana Community discussions.

### Changed
- Updated `pyproject.toml` to include `httpx` as a dependency.
    - Added `httpx>=0.28` to the project dependencies.
    - Updated `uv.lock` file to include new dependencies and their versions, such as `anyio`, `certifi`, `h11`, `httpcore`, `httpx`, `idna`, and `sniffio`.
- Modified `src/arcana_codex/__init__.py` to expose `AsyncArcanaCodexClient`, `ArcanaCodexClient`, and `AdUnitsFetchModel`.
    - Changed the file to import and expose the new client classes and model.  Removed the placeholder `main` function.


----------------------------------------------------------------