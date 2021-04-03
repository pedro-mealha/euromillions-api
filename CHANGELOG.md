# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2021-04-03
### Updated
- All occurrences of `results` to `draws` so it's more consistent.
- Main table `results` to `draws`
- All endpoints from `/results` to `/draws`

## [1.0.0] - 2021-04-03
### Added
- Endpoint to add new contests. This will be used as a cronjob.

## [0.1.0-beta] - 2021-04-02
### Added
- Logic for fetching results data

## [0.4.0-alpha] - 2021-04-01
### Added
- New column contest_id to results table

### Fixed
- Some parsed rows add different strings in setup script

## [0.3.0-alpha] - 2021-03-26
### Added
- Flask files and base endpoints to fetch contest results

## [0.2.1-alpha] - 2021-03-09
### Fixed
- Some syntax issues

## [0.2.0-alpha] - 2021-03-09
### Added
- Python base files
- Setup file to parse euromillions website and populate DB with past results

## [0.1.0-alpha] - 2021-03-09
### Added
- Initial base files

[2.0.0]: https://github.com/WeNeedThePoh/euromillions-api/compare/1.0.0...2.0.0
[1.0.0]: https://github.com/WeNeedThePoh/euromillions-api/compare/0.1.0-beta...1.0.0
[0.1.0-beta]: https://github.com/WeNeedThePoh/euromillions-api/compare/0.4.0-alpha...0.1.0-beta
[0.4.0-alpha]: https://github.com/WeNeedThePoh/euromillions-api/compare/0.3.0-alpha...0.4.0-alpha
[0.3.0-alpha]: https://github.com/WeNeedThePoh/euromillions-api/compare/0.2.1-alpha...0.3.0-alpha
[0.2.1-alpha]: https://github.com/WeNeedThePoh/euromillions-api/releases/tag/0.2.1-alpha
[0.2.0-alpha]: https://github.com/WeNeedThePoh/euromillions-api/commit/db92de7b13f7d28e9023bc52a200c3eadeede1b8
[0.1.0-alpha]: https://github.com/WeNeedThePoh/euromillions-api/commit/a91e5826f0ac1fb9d498d6be15eb5794899c73af
