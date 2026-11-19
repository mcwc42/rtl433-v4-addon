ARG BUILD_FROM
FROM ${BUILD_FROM}

# Build the RTL-SDR Blog driver (the one that supports the V4 / R828D) and
# rtl_433 from source, then drop the build tools. Runtime needs only libusb.
RUN apk add --no-cache libusb \
 && apk add --no-cache --virtual .build build-base cmake git libusb-dev linux-headers pkgconf \
 && git clone --depth 1 https://github.com/rtlsdrblog/rtl-sdr-blog /tmp/rtlsdr \
 && cmake -S /tmp/rtlsdr -B /tmp/rtlsdr/build -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON \
 && cmake --build /tmp/rtlsdr/build -j4 \
 && cmake --install /tmp/rtlsdr/build \
 && git clone --depth 1 https://github.com/merbanan/rtl_433 /tmp/rtl433 \
 && PKG_CONFIG_PATH=/usr/local/lib/pkgconfig cmake -S /tmp/rtl433 -B /tmp/rtl433/build \
 && cmake --build /tmp/rtl433/build -j4 \
 && cmake --install /tmp/rtl433/build \
 && apk del .build \
 && rm -rf /tmp/*

COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]
