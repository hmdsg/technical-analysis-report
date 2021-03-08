import ast
import base64
import binascii
import json
import os
import sys
import urllib.request

FOTA_BASIC_BASE_64 = os.environ['FOTA_BASIC_BASE_64']
FOTA_DOMAIN = os.environ['FOTA_DOMAIN']


def lambda_handler(event, context):
    print(event)

    success_mac_addresses = []
    failed_mac_addresses = []
    ignore_mac_addresses = []
    version_missmatch_mac_addresses = []

    # 最新バージョン取得
    latest_version = fetch_latest_fw_version()

    for record in event["Records"]:
        kinesis = record["kinesis"]
        data = kinesis["data"].encode("ascii")
        decoded_data = base64.b64decode(data).decode(encoding='ascii')
        decoded_dic = ast.literal_eval(decoded_data)
        mac = decoded_dic["clientId"]
        decoded_response = base64.b64decode(
            decoded_dic["response"]).rstrip(b'\x00').hex()

        # コマンド20チェック
        if decoded_response[6:8] != "20":
            print(f"decoded_responseは{decoded_response}でした。")
            ignore_mac_addresses.append(mac)
            continue

        # 成功失敗チェック
        if decoded_response[8:10] != "00":
            failed_mac_addresses.append(mac)
            continue

        version = binascii.a2b_hex(decoded_response[12:]).decode('utf-8')
        print(
            f"Macアドレス: {mac}, Running Partition: {decoded_response[10:12]}, バージョン: {version}")

        # バージョンチェック
        if version == latest_version:
            success_mac_addresses.append(mac)
        else:
            version_missmatch_mac_addresses.append(mac)

    print(f"FW更新成功: {len(success_mac_addresses)}台　{success_mac_addresses}")
    print(f"FW更新失敗: {len(failed_mac_addresses)}台　{failed_mac_addresses}")
    print(
        f"FWバージョン不一致数: {len(version_missmatch_mac_addresses)}台　{version_missmatch_mac_addresses}")
    print(f"処理除外: {len(ignore_mac_addresses)}台　{ignore_mac_addresses}")

    patch_fw_version(success_mac_addresses)


def fetch_latest_fw_version():
    request = urllib.request.Request(
        f"{FOTA_DOMAIN}/fota/smartplug/3/firmwares/latest",
        method="GET",
        headers={
            'Authorization': FOTA_BASIC_BASE_64,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = json.load(response)
            print(body)
            return body["version"]

    except urllib.error.HTTPError as error:
        print(str(error.code) + error.reason)
        print(error)
        sys.exit()


def patch_fw_version(success_mac_addresses):
    if len(success_mac_addresses) == 0:
        print("success_mac_addressesが空なので、更新APIは叩きません。")
        return

    print("更新API叩きます。")
    request = urllib.request.Request(
        f"{FOTA_DOMAIN}/fota/smartplug/3/devices",
        method="PATCH",
        data=json.dumps({"macAddresses": success_mac_addresses}).encode(),
        headers={
            'Authorization': FOTA_BASIC_BASE_64,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = json.load(response)
            print(body)

    except urllib.error.HTTPError as error:
        print(str(error.code) + error.reason)
        print(error)
