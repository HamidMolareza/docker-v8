# ==============================================================================
# First stage build (compile V8)
# ==============================================================================

FROM debian:stable-slim as builder

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update &&\
     DEBIAN_FRONTEND=noninteractive apt-get upgrade -yqq

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get install bison \
                    cdbs \
                    curl \
                    flex \
                    g++ \
                    git \
                    python3 \
                    vim \
                    pkg-config -yqq

RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

ENV PATH="/depot_tools:${PATH}"

RUN fetch v8

WORKDIR /v8

RUN gn gen out/x64.release --args='v8_monolithic=true v8_use_external_startup_data=false is_component_build=false is_debug=false target_cpu="x64" use_goma=false goma_dir="None" v8_enable_backtrace=true v8_enable_disassembler=true v8_enable_object_print=true v8_enable_verify_heap=true'

RUN ninja -C out/x64.release d8

RUN strip out/x64.release/d8

# ==============================================================================
# Second stage build
# ==============================================================================

FROM debian:stable-slim
LABEL maintainer="Hamid Molareza <HamidMolareza@gmail.com>"

ARG DOCKER_VERSION
LABEL org.label-schema.schema-version="$DOCKER_VERSION"

ARG BUILD_DATE
LABEL org.label-schema.build-date="$BUILD_DATE"

LABEL org.label-schema.name="HamidMolareza/d8"
LABEL org.label-schema.description="Google V8 docker image"
LABEL org.label-schema.vcs-url="https://github.com/HamidMolareza/v8-docker"

RUN apt-get update && apt-get upgrade -yqq && \
    DEBIAN_FRONTEND=noninteractive apt-get install curl rlwrap vim -yqq && \
    apt-get clean

WORKDIR /v8

COPY --from=builder /v8/out/x64.release/d8 ./

COPY vimrc /root/.vimrc

COPY entrypoint.sh /entrypoint/

# TODO: rewite entrypoint.sh into python
RUN chmod +x /entrypoint/entrypoint.sh && \
    ln -s /v8/d8 /usr/local/bin/d8

ENTRYPOINT ["/entrypoint/entrypoint.sh"]
