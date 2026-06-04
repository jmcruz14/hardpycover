# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 6/5/2026

### Added

- More class variants

### Changed

- Significant refactoring of the `Hardcover` class by turning `main.py` into an Orchestrator to anticipate the inclusion of future mutation and query methods
- Segmenting of current "query" methods into `queries.py`
- Standardized data fetching and returned objects

### Removed

- urllib3 dependency
- (Temporarily) suspended Pydantic type-checking for data after fetching

## [0.1.2] - 6/2/2026

### Added

- Class variants for `user`

### Changed

- Significantly rewrote the `core` logic to adhere to `sgqlc` logic to account for type checking errors and complex queries
that may be written for the project.
- Updated some declared Pydantic class objects

## [0.1.1a] - 5/27/2026

### Added

- Partially functioning `core` logic
- Working queries for `user_profile`, `user_stats`, `books`, `authors`, and `owned_books`