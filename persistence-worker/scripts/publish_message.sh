#!/bin/bash

base_time=$(date +%s)
data="[]"

for i in $(seq 0 $DATA_ITEMS); do
    ts=$((base_time + i))
    lat="41.$((RANDOM % 1000000))"
    long="-4.$((RANDOM % 1000000))"
    temp=$((15 + RANDOM % 10))

    entry=$(jq -n --arg ts "$ts" --arg lat "$lat" --arg long "$long" --arg temp "$temp" \
        '{"timestamp": $ts, "lat": $lat, "long": $long, "temp": $temp}')

    data=$(echo "$data" | jq --argjson entry "$entry" ". + [\$entry]")
done

payload=$(jq -n \
    --arg mac "1E:E5:89:44:FE:19" \
    --arg imei "123456789012345" \
    --argjson data "$data" \
    '{"mac": $mac, "imei": $imei, "support": ["GPS", "TEMP"], "data": $data}')

sha256=$(echo $payload | jq -S -c '.' | tr -d '\n' | shasum -a 256 | cut -d" " -f1)

final=$(echo "$payload" | jq --arg sha256 "$sha256" ". + {sha256: \$sha256}")

mosquitto_pub -h $MOSQUITTO_HOST -t $MOSQUITTO_TOPIC -m "$final"
echo "✅ Published to $MOSQUITTO_HOST and topic $MOSQUITTO_TOPIC:"
echo "$final"