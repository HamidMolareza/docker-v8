# V8 Docker Image

* Builds the Google JavaScript V8 engine and allows to use the D8 shell
* D8 (Debug8) is V8's own minimalist debug shell (https://v8.dev/docs/d8)

![docker_v8_7 3 255](https://user-images.githubusercontent.com/6396088/50544208-e4f7b000-0bb3-11e9-9c40-b256180b140a.png)

# V8

From https://developers.google.com/v8/:

> V8 is Google’s open source high-performance JavaScript engine, written in C++ and used in Google Chrome, the open source browser from Google, and in Node.js, among others.

# Usage

```
$ docker pull andreburgaud/d8
```

## V8 Enhanced Shell

```
$ docker run --rm -it andreburgaud/d8:9.0.56 shell
Options: --harmony --harmony-shipping --harmony-top-level-await --harmony-intl-dateformat-day-period
         --harmony-sharedarraybuffer --harmony-atomics --harmony-weak-refs --harmony-string-replaceall
         --harmony-logical-assignment --harmony-atomics-waitasync --harmony-relative-indexing-methods
Use quit() or Ctrl-D (i.e. EOF) to exit the D8 Shell
V8 version 9.0.0 (candidate)
d8>
```

* The default V8 shell is wrapped with `rlwrap` (https://github.com/hanslub42/rlwrap) to enhance the experience with the
  REPL (e.g. use arrow keys to recall previous/next lines).

* The `harmony` options are automatically injected via the `entrypoint.sh` script.

* Additional V8 options in addition to the `harmony` ones can be passed at the command line:

```
$ docker run --rm -it andreburgaud/d8 shell --dump-counters
```

Upon exciting the d8 shell, the v8 counters will be dumped to the terminal. The counters are listed alphabetically with
their values.

### Using Multiline

When starting the d8 container with command `shell`, as follow:

```
$ docker run --rm -it andreburgaud/d8 shell
```

You also have the ability to write statements across several lines, by ending lines with a `\` (backslash):

```
d8> function f(n) { \
    print(n); \
}
undefined
d8> f('TEST');
TEST
undefined
d8>
```

### What is Harmony?

When ECMAScript 4 (ES4) was abandoned in 2008, some of its features were rolled into a project codenamed ECMAScript
Harmony. ES6 later renamed ES2015 was the first "ECMAScript Harmony" specification and is also known as "ES6 Harmony".
The V8 harmony options enable specific features that may not yet be part of the default engine features.

### Harmony Flags with Version 9.x

The following flags are enabled when starting the D8 repl `docker run --rm -it andreburgaud/d8 shell`:

```
--harmony                             (enable all completed harmony features)
--harmony-shipping                    (enable all shipped harmony features)
--harmony-top-level-await             (enable "harmony top level await")
--harmony-intl-dateformat-day-period  (enable "Add dayPeriod option to DateTimeFormat")
--harmony-sharedarraybuffer           (enable "harmony sharedarraybuffer")
--harmony-atomics                     (enable "harmony Atomics.waitAsync")
--harmony-weak-refs                   (enable "harmony weak references")
--harmony-string-replaceall           (enable "harmony String.prototype.replaceAll")
--harmony-logical-assignment          (enable "harmony logical assignment")
--harmony-atomics-waitasync           (enable "harmony Atomics.waitAsync")
--harmony-relative-indexing-methods   (enable "harmony relative indexing methods")
```

## Help

```
$ docker run --rm -it andreburgaud/d8 help
```

Display the commands available via the docker container.

## Default V8 Shell

```
$ docker run --rm -it andreburgaud/d8
```

## Internal V8 help

```
$ docker run --rm -it andreburgaud/d8 --help
```

## Start D8 with custom options

```
$ docker run --rm -it andreburgaud/d8 --dump-counters
```

## Executing a JavaScript file

Assuming that the following `hello.js` file is in the folder `examples` of your current working directory:

```javascript
console.log('Hello World!');
```

Execute:

```
docker run --rm -it -v $PWD/examples:/examples/ andreburgaud/d8 /examples/hello.js
Hello World!
```

# Build Local Image

```
$ git clone https://github.com/andreburgaud/docker-v8.git
$ cd docker-v8
$ docker build -t d8 .
```

**Note**: the compilation may take some time depending on your hardware. For example it takes about 30 minutes on a
3.5GHz four core iMac with 24GB of RAM.

# Resources

* https://github.com/v8/v8
* https://github.com/v8/v8/wiki
* https://github.com/v8/v8/wiki/Building-with-GN
* https://en.wikipedia.org/wiki/ECMAScript
* https://gist.github.com/kevincennis/0cd2138c78a07412ef21

# MIT License

See the license file
