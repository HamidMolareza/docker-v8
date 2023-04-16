# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## 0.1.0 (2023-04-16)


### ⚠ BREAKING CHANGES

* **dockerfile:** move `entrypoint.sh` to `/entrypoint/entrypoint.sh`
* remove V8_VERSION and add DOCKER_VERSION, BUILD_DATE Args

### Features

* **dockerfile:** move `entrypoint.sh` to `/entrypoint/entrypoint.sh` ([4610f8e](https://github.com/HamidMolareza/v8-docker/commit/4610f8ecf9533ef185ffadf777d750a3a0f82266))
* **Dockerfile:** Version and symlinks ([7dd8a2c](https://github.com/HamidMolareza/v8-docker/commit/7dd8a2c898f6f4bc06f916abea94a9d8a317e2f6))
* **Entrypoint:** Added numeric separator to the default flags in the shell ([aa899b9](https://github.com/HamidMolareza/v8-docker/commit/aa899b9d27d451b9e2f454872d8f988cea1ab98b))
* **Entrypoint:** New commands and UX improvements ([14dee8a](https://github.com/HamidMolareza/v8-docker/commit/14dee8a848a984083bf736f3f6dcca50c88c8c07))
* **Makefile:** Validate if environment variable with tag is set ([40752b1](https://github.com/HamidMolareza/v8-docker/commit/40752b17c0166cbb1e6700f21895d85b84d02863))
* update ARGs and LABELs in Dockerfile ([937599b](https://github.com/HamidMolareza/v8-docker/commit/937599b41580a3a245016abd41a244441057afaf))


### Documents

* add Payadel README template ([ef9fffd](https://github.com/HamidMolareza/v8-docker/commit/ef9fffd57663ef7d57263dd02d9a86d972bcf68a))
* Added build section ([14ec8df](https://github.com/HamidMolareza/v8-docker/commit/14ec8df9b44cc0c2b641e9dcf6d73a5665d9d0b0))
* **README:** Added multiline documentation ([af61a27](https://github.com/HamidMolareza/v8-docker/commit/af61a271a54af7944bab2e60051019990a17d69e))
* **README:** Removed build badge ([598c274](https://github.com/HamidMolareza/v8-docker/commit/598c274d5e9581e215b3476e61cfdfcd53a97ef6))
* **README:** Updated name of image to full qualified name ([b401a10](https://github.com/HamidMolareza/v8-docker/commit/b401a101b2cb8ed540e53fda876092985f47bbc6))
* **README:** Updated usage instructions ([b812415](https://github.com/HamidMolareza/v8-docker/commit/b81241576ef5c0e497b8d9620311a36103ee0330))


### Fixes

* **$compile:** Missed new line continuation ([fe4c6bf](https://github.com/HamidMolareza/v8-docker/commit/fe4c6bf71d6fe9142d762852e2a1fb2a10725de8))
* **dockerfile:** move `entrypoint.sh` to `/entrypoint/entrypoint.sh` ([90086ee](https://github.com/HamidMolareza/v8-docker/commit/90086ee2d3223fd3a4feceb8e38fa0320eefe786))
* **Entrypoint:** Updated list of harmony options ([7ed9e4b](https://github.com/HamidMolareza/v8-docker/commit/7ed9e4b4c5c51b5480e1cd1c6bade0b8fdf88b21))
* **Entrypoint:** Updated name of the image to include the full qualified name ([167490f](https://github.com/HamidMolareza/v8-docker/commit/167490f07682bb1337db9b90fcb2119dde919f9f))
* install python3 in docker file ([2d8de73](https://github.com/HamidMolareza/v8-docker/commit/2d8de7309b0a8f0e0b4cf55097067289b8940433))


### Development: CI/CD, Build, etc

* add `cache-from` and `cache-to` parameters to `docker/build-push-action` ([8c187b2](https://github.com/HamidMolareza/v8-docker/commit/8c187b2937c58fa1771625ff2fc87eee8f5908eb))
* add actions:build script to package.json for run `build-docker.yaml` ([5af3800](https://github.com/HamidMolareza/v8-docker/commit/5af380096acee3784107a81aea5afcdab0ac8a79))
* add entrypoint.sh ([b21ba7c](https://github.com/HamidMolareza/v8-docker/commit/b21ba7c0eb993bb5ebdf1f29d197267d4f85e028))
* add GitHub action for build docker ([1713a8a](https://github.com/HamidMolareza/v8-docker/commit/1713a8ab5fa46881c8b90566d81726348e80e893))
* add install-package.sh ([01c93f9](https://github.com/HamidMolareza/v8-docker/commit/01c93f969ff4bdce50a41ce8ae084c5b4ce0f119))
* add name to build-docker.yaml ([5e40783](https://github.com/HamidMolareza/v8-docker/commit/5e407833465dec0458c55db1fded98593857eb6e))
* **Build:** Added Makefile ([ddfa74c](https://github.com/HamidMolareza/v8-docker/commit/ddfa74ce10f89276251ef290b24966f67b5ba22d))
* **Build:** Tag the image prior to pushing it ([3c11fcf](https://github.com/HamidMolareza/v8-docker/commit/3c11fcfd7ff816ee043684314311a4ced756dd33))
* correct github action name ([a0e6ccb](https://github.com/HamidMolareza/v8-docker/commit/a0e6ccbbf1a6e5f94a63fb77fc8f5e0e29c31806))
* **Dockerfile:** Removed unneeded packages from build stage ([3aba8cf](https://github.com/HamidMolareza/v8-docker/commit/3aba8cf99c6f388afee65b7cb75f49b183befbd1))
* fix `Set build arguments` step ([ee5862e](https://github.com/HamidMolareza/v8-docker/commit/ee5862ec0fb673ac5ca6d9024e16b2863383fc49))
* fix build-docker.yaml bug ([72e9420](https://github.com/HamidMolareza/v8-docker/commit/72e9420364cbfeb42449afcbe5fa29c89d4527fb))
* fix docker remote cache in actions ([bfa8759](https://github.com/HamidMolareza/v8-docker/commit/bfa875918b71547c99dd8a7c79226f96449b7233))
* fix Makefile ([2d12050](https://github.com/HamidMolareza/v8-docker/commit/2d12050810ca3b8e4a4824019f4a248af1c7c0ac))
* fix names ([971ca46](https://github.com/HamidMolareza/v8-docker/commit/971ca46777ac8f937968d1ce0af69ae36a27cc0a))
* **Ignore:** Added Docker ignore file ([52e7c70](https://github.com/HamidMolareza/v8-docker/commit/52e7c7016a6e881a4dfff18e54f1dc59ac1dead1))
* **Makefile:** Added a deploy task ([394c048](https://github.com/HamidMolareza/v8-docker/commit/394c048d030bca0b89d954ffa61db2e38ccab68d))
* **Makefile:** Added push for tag 'latest' ([dfb41eb](https://github.com/HamidMolareza/v8-docker/commit/dfb41eb06911052c4f48a0744562a9d7f864d6e1))
* **Makefile:** Added push to github ([92103ee](https://github.com/HamidMolareza/v8-docker/commit/92103ee06498f60b6117bc894ddd1ac850ee2626))
* **Makefile:** Remove github task ([e566daf](https://github.com/HamidMolareza/v8-docker/commit/e566daf0bd666b61dc5d883ced76e6fc32e05191))
* **Makefile:** Replace hard-coded image name with variable IMAGE ([1cd3843](https://github.com/HamidMolareza/v8-docker/commit/1cd3843e8696780a4f44ca00b0ef4ccf2fd3ae17))
* **Makefile:** Update .PHONY list ([b1c390a](https://github.com/HamidMolareza/v8-docker/commit/b1c390a60fc83c38a4411cf9d6fdafbe9bf56ef5))
* **Makefile:** Updated to 6.8.260 ([881ee20](https://github.com/HamidMolareza/v8-docker/commit/881ee208323fd94e955e20901cfe364324bf4622))
* **Makefile:** Use environment variable for Docker image tag ([e05003a](https://github.com/HamidMolareza/v8-docker/commit/e05003acb82da84ccc466b7809a6883effadcd0b))
* print current branch name in build-docker.yaml ([2917c88](https://github.com/HamidMolareza/v8-docker/commit/2917c881ac14e95830e584585afa855028292fba))
* **release:** add `Docker` section in release.yaml action ([8a07085](https://github.com/HamidMolareza/v8-docker/commit/8a07085601e2732d1832754e68c67eaec230e798))
* remove cache system in actions ([b9bf776](https://github.com/HamidMolareza/v8-docker/commit/b9bf7764ccc24d06df321e0891585331634c2afd))
* remove excess codes from buid-docker.yaml ([882d075](https://github.com/HamidMolareza/v8-docker/commit/882d07506afac659b3123192f3f1b5b217f24746))
* update .dockerignore ([0661e4a](https://github.com/HamidMolareza/v8-docker/commit/0661e4a990ea5dea3f93455dd066ce7dc5e3a714))
* update .dockerignore ([5fd3079](https://github.com/HamidMolareza/v8-docker/commit/5fd307910e7a89390bc7587dcb4b0b02ab8c3e70))
* update build-docker action base new Docker file ([d240993](https://github.com/HamidMolareza/v8-docker/commit/d240993582627f1ab770137a8894ee8f544c1681))
* update Makefile base new Dockerfile ([6660aaa](https://github.com/HamidMolareza/v8-docker/commit/6660aaadcbb8b719db92f06268506ad13f945939))
* update pyproject.toml dependencies ([d5560d0](https://github.com/HamidMolareza/v8-docker/commit/d5560d08940ef2659106aeb815206e4bfd27249e))
* update release.yaml action ([d2361bf](https://github.com/HamidMolareza/v8-docker/commit/d2361bfde1039b08a90c2cc80a74ee90c1a5361e))
* use `build-push-action` in github action ([c7839aa](https://github.com/HamidMolareza/v8-docker/commit/c7839aa524bb6ff8cba7c198a6b19b2887b2c3d2))
