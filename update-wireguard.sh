#!/bin/bash
set -e

BASE_URL="http://localhost:8000"
VPN_UUID="8097b09b-e57a-4b27-8e2e-f2ea9ea809f3"
VPN_KEY="gWhPJzDpfGeC8pXJURcbD70ZOdJWzofl"
# make sure this directory is writable by the user which calls the script
CONF_DIR="/etc/wireguard"

# do not modify these vars
_VPN_URL_PATH="$BASE_URL/controller/vpn"
_VPN_CHECKSUM_URL="$_VPN_URL_PATH/checksum/$VPN_UUID/?key=$VPN_KEY"
_VPN_DOWNLOAD_URL="$_VPN_URL_PATH/download-config/$VPN_UUID/?key=$VPN_KEY"
_WORKING_DIR="$CONF_DIR/.openwisp"
_CHECKSUM_FILE="$_WORKING_DIR/checksum"
_CONF_TAR="$_WORKING_DIR/conf.tar.gz"

mkdir -p $_WORKING_DIR

check_config() {
    _latest_checksum=$(curl -s $_VPN_CHECKSUM_URL)

    if [ -f "$_CHECKSUM_FILE" ]; then
        _current_checksum=$(cat $_CHECKSUM_FILE)
    else
        _current_checksum=''
    fi

    if [ "$_current_checksum" != "$_latest_checksum" ]; then
        echo 'Configuration changed, downloading new configuration...'
        update_config
    fi
}

update_config() {
    curl -s $_VPN_DOWNLOAD_URL > "$_CONF_TAR"
    echo $_latest_checksum > $_CHECKSUM_FILE
    echo 'Configuration downloaded, extracting it...'
    tar -zxvf $_CONF_TAR -C $CONF_DIR > /dev/null

    for file in $CONF_DIR/*.conf; do
        [ -e "$file" ] || continue
        filename=$(basename $file)
        interface="${filename%.*}"
        echo "Reloading wireguard interface $interface with config file $file..."
        sudo wg syncconf $interface $file
    done

    ./apply_vxlan.py "$CONF_DIR/vxlan.json"
}

check_config
