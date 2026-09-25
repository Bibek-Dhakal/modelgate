# Changelog

## [0.2.0](https://github.com/Bibek-Dhakal/modelgate/compare/v0.1.0...v0.2.0) (2026-09-25)


### Features

* **inference:** overhaul to dynamic artifact loading and JSON schema validation ([0300539](https://github.com/Bibek-Dhakal/modelgate/commit/03005396ef5ec2808a57c981d99c4c9f66aade9d))
* setup initial core project structure and CI/CD pipeline ([dd96475](https://github.com/Bibek-Dhakal/modelgate/commit/dd964754db9276de71b419960ce0a9f2a01be969))


### Bug Fixes

* **config:** strip inline comments from environment variables to prevent docker parsing errors ([3501f63](https://github.com/Bibek-Dhakal/modelgate/commit/3501f63ce9fcb403247736a8e61b0cbabcc3b773))
* **tests:** correct assertions for string predictions and suppress sklearn warnings ([26bbebc](https://github.com/Bibek-Dhakal/modelgate/commit/26bbebc060e6bc97ed0d07cfb6603ff070f6411a))


### Miscellaneous Chores

* update pyproject warnings filter and add .docker ignore file ([a489b50](https://github.com/Bibek-Dhakal/modelgate/commit/a489b50157884032fb7f193b0aa88037b9e2ba3a))


### Documentation

* **project:** remove all mock references and update architecture diagrams ([581ce92](https://github.com/Bibek-Dhakal/modelgate/commit/581ce92630673b61e868a171dedc22eebbfdd136))


### Code Refactoring

* **inference:** replace mock logic with default public iris model ([7ff3c3c](https://github.com/Bibek-Dhakal/modelgate/commit/7ff3c3cb2044961b6c507476612ff3e744f99446))
