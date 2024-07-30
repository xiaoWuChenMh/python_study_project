from adbutils import adb, AdbClient

for d in adb.device_list():
    print(d.serial)

client = AdbClient(host="127.0.0.1", port=5037)
a = {}
for info in client.list():
    a[info.state] = info
    print(info)
print(a)
client.connect('emulator-5556')
print(client.device_list())
