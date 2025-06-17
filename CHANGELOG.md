## [1.9.1](https://github.com/Sigmanor/uakino.club_bot/compare/v1.9.0...v1.9.1) (2025-06-17)


### Bug Fixes

* **config:** update uakino domain to .best ([1aed599](https://github.com/Sigmanor/uakino.club_bot/commit/1aed599f245906b4780f066dec8ce1d6cdf823df))

# [1.9.0](https://github.com/Sigmanor/uakino.club_bot/compare/v1.8.3...v1.9.0) (2025-04-13)


### Features

* add disabled button handler for content search ([c4e9607](https://github.com/Sigmanor/uakino.club_bot/commit/c4e9607329e97fed06f2211a2488b9066447af6d))
* improve the notification mechanism to send a temporary message that is deleted after use ([2d2c302](https://github.com/Sigmanor/uakino.club_bot/commit/2d2c302c6472fae906ac4064d844f84d5ee3caaa))

## [1.8.3](https://github.com/Sigmanor/uakino.club_bot/compare/v1.8.2...v1.8.3) (2025-04-02)


### Bug Fixes

* improve bot restart and timeout handling ([ef1f162](https://github.com/Sigmanor/uakino.club_bot/commit/ef1f162fbfedaac3685472123a3c8bef4b3470e0))

## [1.8.2](https://github.com/Sigmanor/uakino.club_bot/compare/v1.8.1...v1.8.2) (2025-03-28)


### Bug Fixes

* correct base directory path in Database initialization ([91db47b](https://github.com/Sigmanor/uakino.club_bot/commit/91db47b84a9070ce4862c7f6b8cdcb803023e1b8))
* enhance error handling and bot restart logic for network issues ([5e2eb97](https://github.com/Sigmanor/uakino.club_bot/commit/5e2eb9753106207c09c2c10b55569f1a904d1924))

## [1.8.1](https://github.com/Sigmanor/uakino.club_bot/compare/v1.8.0...v1.8.1) (2025-03-13)


### Bug Fixes

* add missing logger initialization in health_check function ([7c0d146](https://github.com/Sigmanor/uakino.club_bot/commit/7c0d146fcb7891f4b53805321b3feae3538e5f11))

# [1.8.0](https://github.com/Sigmanor/uakino.club_bot/compare/v1.7.3...v1.8.0) (2025-02-28)


### Bug Fixes

* add missing asyncio import and update import statements to use relative paths ([6f5fde8](https://github.com/Sigmanor/uakino.club_bot/commit/6f5fde845c6298fe35e04a48044d854ff387c6c3))
* update Dockerfile to use module syntax for bot execution ([cdaf275](https://github.com/Sigmanor/uakino.club_bot/commit/cdaf2756069856d793c2f138221fa11429f36aa2))
* update import statements to use relative paths in commands.py ([f01e696](https://github.com/Sigmanor/uakino.club_bot/commit/f01e696d702ea3180ffb1b7f829619c859e26b8b))


### Features

* add __init__.py to src directory for package initialization ([9bad981](https://github.com/Sigmanor/uakino.club_bot/commit/9bad98189885d1fdfa80a3abfb4f29a835a16df8))

## [1.7.3](https://github.com/Sigmanor/uakino.club_bot/compare/v1.7.2...v1.7.3) (2025-02-28)


### Bug Fixes

* allow manual triggering of release workflow ([8353253](https://github.com/Sigmanor/uakino.club_bot/commit/835325345ab3c9fa0b0095b774b18d1e0e911446))
* update .dockerignore to exclude database files ([42316d4](https://github.com/Sigmanor/uakino.club_bot/commit/42316d4179607cc27927b43652325574643bd87b))
* update .gitignore to exclude database directory ([0bff07c](https://github.com/Sigmanor/uakino.club_bot/commit/0bff07c016b3cbcb521bf7830a592720702ecfa2))

## [1.7.2](https://github.com/Sigmanor/uakino.club_bot/compare/v1.7.1...v1.7.2) (2025-02-20)


### Bug Fixes

* enhance another_handler to generate new content and update inline keyboard ([1a5429e](https://github.com/Sigmanor/uakino.club_bot/commit/1a5429e34b814c411fd1479eea435c8bdb08e30d))
* simplify inline keyboard construction and improve logging format ([c12214c](https://github.com/Sigmanor/uakino.club_bot/commit/c12214c3e65d2bc4501e41dfb04672752bd1ea2c))
* streamline content fetching by removing retry logic and improving pagination handling ([f5bd6bb](https://github.com/Sigmanor/uakino.club_bot/commit/f5bd6bbf46e3f3e21dc743775ab30e160515007c))

## [1.7.1](https://github.com/Sigmanor/uakino.club_bot/compare/v1.7.0...v1.7.1) (2025-02-20)


### Bug Fixes

* enhance deployment script with error handling and cleanup steps ([c9f6b2d](https://github.com/Sigmanor/uakino.club_bot/commit/c9f6b2d84b4bc08b60ace7e3633566fb1774989f))
* handle Forbidden error in error handler ([9decce5](https://github.com/Sigmanor/uakino.club_bot/commit/9decce58e0c128722e96dd4ab6a72a991f03efef))
* implement retry logic for content fetching and enhance error handling ([72f8caf](https://github.com/Sigmanor/uakino.club_bot/commit/72f8caf1c80e5e69328298fd2cc21533bb37440d))
* rename deployment workflow for clarity ([bf16937](https://github.com/Sigmanor/uakino.club_bot/commit/bf169371e4fe0f35efbea68697f3b95d430337c4))
* update deployment script to remove old installation without sudo ([0e75f2d](https://github.com/Sigmanor/uakino.club_bot/commit/0e75f2da541ba78037ba87f88af7675b28d866af))

# [1.7.0](https://github.com/Sigmanor/uakino.club_bot/compare/v1.6.0...v1.7.0) (2025-02-16)


### Features

* enhance error handling and improve logging in bot.py ([e2caeec](https://github.com/Sigmanor/uakino.club_bot/commit/e2caeecc481cb6120e429a20b331f721d1f69840))

# [1.6.0](https://github.com/Sigmanor/uakino.club_bot/compare/v1.5.0...v1.6.0) (2025-02-15)


### Features

* update application version to 1.6.0 to compare inapp ver with semantic-release ([cc2bd19](https://github.com/Sigmanor/uakino.club_bot/commit/cc2bd19e10ca854565908efd48370905004dd53d))

# [1.5.0](https://github.com/Sigmanor/uakino.club_bot/compare/v1.4.0...v1.5.0) (2025-02-15)


### Features

* bump application version to 1.4.0 ([9d029ff](https://github.com/Sigmanor/uakino.club_bot/commit/9d029ff1edde5ae5c92395e1e47fcaba264db112))

# [1.4.0](https://github.com/Sigmanor/uakino.club_bot/compare/v1.3.0...v1.4.0) (2025-02-15)


### Features

* add CHANGELOG.md for tracking project updates and version history ([6484e6d](https://github.com/Sigmanor/uakino.club_bot/commit/6484e6da36ddb8719d2df0e80cc3106bb74de0b8))
* add GitHub Actions workflow for automated releases using semantic release ([a577310](https://github.com/Sigmanor/uakino.club_bot/commit/a57731075589bd9cc0c4a8d0a2ae43f155c6f0da))
* add package.json for semantic release and changelog management ([a5e0e94](https://github.com/Sigmanor/uakino.club_bot/commit/a5e0e9476ebd56f68c4b4ae10124cf8bcb96bcc5))
* add semantic release configuration for automated versioning and changelog generation ([a2931f4](https://github.com/Sigmanor/uakino.club_bot/commit/a2931f4fbde40bc27efa124cec9528ebe9de8bce))
* update GitHub Actions workflow to include permissions and correct token usage ([2dc4c7f](https://github.com/Sigmanor/uakino.club_bot/commit/2dc4c7fde6dbb96a093bf312b87e27deab799ac6))
