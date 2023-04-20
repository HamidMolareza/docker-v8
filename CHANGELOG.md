# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [0.2.1](https://github.com/HamidMolareza/v8-docker/compare/v0.2.0...v0.2.1) (2023-04-20)


### Tests

* update `samples` command tests ([fbd0249](https://github.com/HamidMolareza/v8-docker/commit/fbd0249a5617547534b4b8c580a546bdb8abe1ee))


### Documents

* add `Change Entrypoint` section to README.md ([923916a](https://github.com/HamidMolareza/v8-docker/commit/923916ab0d92165848c74b4c2da31a1e04dc34a0))
* update CONTRIBUTING.md ([7e5d1d4](https://github.com/HamidMolareza/v8-docker/commit/7e5d1d497803053bbff716b53f5b968e86b975a0))
* update README.md ([f52c8a6](https://github.com/HamidMolareza/v8-docker/commit/f52c8a673cc5007b199589b6d7555462b53b5db6))


### Fixes

* improve Dockerfile to reduce image size ([2a6c42e](https://github.com/HamidMolareza/v8-docker/commit/2a6c42ee4d99a924a9e3190c1d7251800d5bf47a))
* update `samples` command texts ([b774c3f](https://github.com/HamidMolareza/v8-docker/commit/b774c3fa64cf69774acedf8b6adaf1f455e7ab5a))

## [0.2.0](https://github.com/HamidMolareza/v8-docker/compare/v0.1.1...v0.2.0) (2023-04-19)


### ⚠ BREAKING CHANGES

* **commands:** Display errors is changed and if d8 fails, we return that code as exit code

### Features

* add about command ([b240c24](https://github.com/HamidMolareza/v8-docker/commit/b240c24595f65cbbdd01378876d4daead893ab32))
* add more sample ([d8cf72d](https://github.com/HamidMolareza/v8-docker/commit/d8cf72d77e8194b2fbc956a00d888ed9a80312a2))
* recognition of commands regardless of uppercase and lowercase letters ([7cb1e46](https://github.com/HamidMolareza/v8-docker/commit/7cb1e468cfbb9c6eef427a4009e05f932e4fdaeb))


### Documents

* add docstring ([f4c7f3c](https://github.com/HamidMolareza/v8-docker/commit/f4c7f3c2614e300cabf0318120df42614dbf8e6b))


### Refactors

* reformat docs and codes ([b191eb2](https://github.com/HamidMolareza/v8-docker/commit/b191eb2b46be07140548d73c35e88dca55f208a1))


### Fixes

* `main` function accepts args and returns int as exit code ([313804e](https://github.com/HamidMolareza/v8-docker/commit/313804e1710604ec4579cfdcc8e94a97a19bbf92))
* add message to FailResult ([a5d666c](https://github.com/HamidMolareza/v8-docker/commit/a5d666c44b1e46008fd5d8272c1650a641c42a7d))
* add more validation for `log_result` ([2f8f162](https://github.com/HamidMolareza/v8-docker/commit/2f8f1620b633e111e702822bcfb67a9f3fef20ad))
* **commands:** add more validations for commands ([5d063ad](https://github.com/HamidMolareza/v8-docker/commit/5d063ada226f3e08c28d1c15c639770daf78293b))
* **commands:** fix return codes from d8 ([33c289c](https://github.com/HamidMolareza/v8-docker/commit/33c289c73b55b4deba4c9e03cc6cce97556747f2))
* **commands:** improve `command_bash` ([f484f41](https://github.com/HamidMolareza/v8-docker/commit/f484f41d62caa72eb78530eca4fbd7f4196ddeda))
* **commands:** improve `command_samples` ([9784a43](https://github.com/HamidMolareza/v8-docker/commit/9784a43699a5401834aa2c1cbf212d64e23f278f))
* **commands:** improve `command_shell` ([2522247](https://github.com/HamidMolareza/v8-docker/commit/2522247de4f406b6649201e300b3697935c21d24))
* **commands:** improve validation, more log, display errors and fix exit code when d8 fails ([28961b9](https://github.com/HamidMolareza/v8-docker/commit/28961b935253fcc0b9b4432fb436c29131116a9d))
* **entrypoint:** remove global logger to make it easy to test ([9b544c5](https://github.com/HamidMolareza/v8-docker/commit/9b544c51cd81d9bb49296be20d6c0046c7110480))
* fix `log_result` return ([a6b1e34](https://github.com/HamidMolareza/v8-docker/commit/a6b1e3412ce7869f239cb0c8c73d5320005cd016))
* fix command_about ([a6deb03](https://github.com/HamidMolareza/v8-docker/commit/a6deb03c3387bc80a96998ac752f8688a694e2aa))
* fix log errors ([46dcbaa](https://github.com/HamidMolareza/v8-docker/commit/46dcbaa35395c4e9c92a4d301756a7050de7d2a0))
* improve `convert_code_to_result` ([885b45e](https://github.com/HamidMolareza/v8-docker/commit/885b45e58a67d9f01656531ec5ca63aa5d8623b9))
* improve `log_error` ([19efa33](https://github.com/HamidMolareza/v8-docker/commit/19efa33836371fe14b9900e44f9f4cf4412d8c45))
* improve `log_result` ([0d5c339](https://github.com/HamidMolareza/v8-docker/commit/0d5c3393020647f97b6ac3ec4882fe767b0f3d8f))
* log unhandled exceptions from `_inner_main` & other bugs ([52450bc](https://github.com/HamidMolareza/v8-docker/commit/52450bc295aaf80a8f75bfb3ef50acad089c8056))
* make logger name optional ([a1aad31](https://github.com/HamidMolareza/v8-docker/commit/a1aad314ef21272f4f4cecd5e915fb381244b6f6))
* make message optional in FailResult.py ([fa6ca7d](https://github.com/HamidMolareza/v8-docker/commit/fa6ca7d6bace3fbef22d494366d995182596fff8))
* use `class_properties_to_str` instead of `log_class_properties` ([e0354de](https://github.com/HamidMolareza/v8-docker/commit/e0354de26ddd2f1a19bbcbc8f879c4f7d206cb5b))
* use `validate_func_params` for validations ([4d35532](https://github.com/HamidMolareza/v8-docker/commit/4d3553234a648488dabda50b6cccb5a7d6bdaa69))
* use Schema package for validate `command_about` parameters ([433ca13](https://github.com/HamidMolareza/v8-docker/commit/433ca13d6d86d58d529a9603b0f65472f22324ca))
* use Schema package for validate `command_bash` parameters ([65a7efb](https://github.com/HamidMolareza/v8-docker/commit/65a7efb9b0c62ef1f585661de22fb632402035f7))
* use Schema package for validate `command_d8` parameters ([3406fd0](https://github.com/HamidMolareza/v8-docker/commit/3406fd016069379b8a3904348ead163b80700f92))
* use Schema package for validate `command_run` ([af1cbd9](https://github.com/HamidMolareza/v8-docker/commit/af1cbd9535710ea973a0a04c1f467be19faa127d))
* use Schema package for validate `command_samples` parameters ([0a466e0](https://github.com/HamidMolareza/v8-docker/commit/0a466e0159d55bd2d4199533568b94e9ad23ed92))
* use Schema package for validate `command_shell` parameters ([f4ddc4c](https://github.com/HamidMolareza/v8-docker/commit/f4ddc4c822fe735150ddfd55d6db6421b47bae3d))
* use Schema package for validate `main` parameters ([383c487](https://github.com/HamidMolareza/v8-docker/commit/383c4874b810931b75df4c45a17e39fe310fd81a))


### Tests

* add test for `test_get_support_message` ([951e5f5](https://github.com/HamidMolareza/v8-docker/commit/951e5f548da99c6989b8774936ecbae680988ab2))
* add test for cli_parser.py ([c31e9f0](https://github.com/HamidMolareza/v8-docker/commit/c31e9f03fc0b1a8eb95f78e832aaf0d3853e693b))
* add test for run command ([67e0d52](https://github.com/HamidMolareza/v8-docker/commit/67e0d524f9f0956d369d8ca0b7d66a37fe40546f))
* add tests for `Logger` class ([38fb9a1](https://github.com/HamidMolareza/v8-docker/commit/38fb9a1950ec9cb7053765f0c3f4fe228f3103e0))
* add tests for entrypoint.py ([dbb402f](https://github.com/HamidMolareza/v8-docker/commit/dbb402f92819d3ac70b328f602f8e8c0d6c0b893))
* add tox ([24a699b](https://github.com/HamidMolareza/v8-docker/commit/24a699b6119a3a21fbe8dd1cbca3e358245b8acf))
* **commands:** add tests for `command_d8` ([4bb05cb](https://github.com/HamidMolareza/v8-docker/commit/4bb05cb57f8c3e40b31398f96d49b219d163c4cc))
* **commands:** add tests for `command_samples`, `test_command_about_ok` ([f87c4f3](https://github.com/HamidMolareza/v8-docker/commit/f87c4f3d5fc02fef63913a82dc3bbd5bfe508d92))
* complete coverage ([eab6433](https://github.com/HamidMolareza/v8-docker/commit/eab6433e64856a00f910b9bc8009a2f132011be5))
* fix errors ([ed21e76](https://github.com/HamidMolareza/v8-docker/commit/ed21e76d33cdc2442cc883f00349e77d741c9538))


### Development: CI/CD, Build, etc

* add codeql.yml ([8030f3f](https://github.com/HamidMolareza/v8-docker/commit/8030f3f3e2e486ca465b52ddc68493e30d2890c7))
* add coverage ([67be835](https://github.com/HamidMolareza/v8-docker/commit/67be8356fd9edd1551927f89836373c842e940ea))
* support multi tags in push-docker.yaml ([353a347](https://github.com/HamidMolareza/v8-docker/commit/353a34704dc3a06e0f34a9ffe3e2635a3acda22e))
* update poetry dependencies before push ([c40369b](https://github.com/HamidMolareza/v8-docker/commit/c40369b5b958c468a908dc10fd2b0cf5ee4d4b42))

### [0.1.1](https://github.com/HamidMolareza/v8-docker/compare/v0.1.0...v0.1.1) (2023-04-16)

### Fixes

* **dockerfile:** reduce
  size ([e65e8fd](https://github.com/HamidMolareza/v8-docker/commit/e65e8fdc865c3383447c31ab12747be080f907eb))
* fix samples
  command ([4caa02d](https://github.com/HamidMolareza/v8-docker/commit/4caa02d99347e50d63609d976edcc3dc54c9448b))

### Development: CI/CD, Build, etc

* add build-push-docker to
  Makefile ([a1e5e00](https://github.com/HamidMolareza/v8-docker/commit/a1e5e0019a87ba516ff9346b364a40efb5caa263))
* fix push-docker.yaml: make push
  true ([f88e08b](https://github.com/HamidMolareza/v8-docker/commit/f88e08b869c0d315c136ccf9e12851d18472a698))
* update package.json
  scripts ([a0c5b64](https://github.com/HamidMolareza/v8-docker/commit/a0c5b64702c99e501fc0fc7de236fabb5693a0e4))
* update poetry version in
  release.yaml ([c3bdcc8](https://github.com/HamidMolareza/v8-docker/commit/c3bdcc8a7ebde170465cab080e4246d7fb4af999))
* 
