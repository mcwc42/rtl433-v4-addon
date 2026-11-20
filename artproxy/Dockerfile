ARG BUILD_FROM
FROM ${BUILD_FROM}
RUN apk add --no-cache python3 ca-certificates
COPY proxy.py /proxy.py
CMD [ "python3", "/proxy.py" ]
