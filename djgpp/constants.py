
# https://developer.android.com/reference/android/Manifest.permission_group
GROUPS = {
    'calendar': [],
    'camera': [],
    'contacts': ['accounts'],
    # https://github.com/r3gis3r/SampleCSipSimpleApp/blob/master/SampleCSipSimpleApp/AndroidManifest.xml
    'cost money': ['sip'],
    'location': [],
    'microphone': ['audio'],
    # why android manifest doesn't have this category?
    'network': ['connections', 'wifi', 'bluetooth', 'internet'],
    'phone': ['call'],
    'sensors': ['vibrate'],
    'sms': ['mms', 'cell'],
    'storage': ['usb'],
    # https://github.com/chrislacy/LauncherJellyBean/blob/master/AndroidManifest.xml
    'system tools': ['settings', 'uninstall', 'install'],
}

UPPERCASE = {
    'gps': 'GPS',
    'sms': 'SMS',
    'mms': 'MMS',
    'WIFI': 'Wi-Fi',
}

NULL_OBJECT_NAME = 'Other'
