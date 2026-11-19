#!/usr/bin/with-contenv bashio
# Publishes decoded 433 MHz events to MQTT at rtl_433/rtl433v4/events, which the
# rtl_433 MQTT Auto Discovery bridge (already installed) turns into HA sensors.
export LD_LIBRARY_PATH="/usr/local/lib"

FREQ="$(bashio::config 'frequency')"
MQTT_HOST="$(bashio::services mqtt 'host')"
MQTT_PORT="$(bashio::services mqtt 'port')"
MQTT_USER="$(bashio::services mqtt 'username')"
MQTT_PASS="$(bashio::services mqtt 'password')"

bashio::log.info "rtl_433 V4: freq ${FREQ}, MQTT ${MQTT_HOST}:${MQTT_PORT}"

exec rtl_433 -f "${FREQ}" \
  -F "mqtt://${MQTT_HOST}:${MQTT_PORT},user=${MQTT_USER},pass=${MQTT_PASS},retain=1,events=rtl_433/rtl433v4/events" \
  -M time:iso -M level
