from dateutil.parser import parse
import os


def get_naglist():
    return os.path.expanduser("~/.naglist")


def get_nags():
    nags = []
    with open(get_naglist()) as nagfile:
        for l in nagfile:
            if "|" in l:
                nag_parts = l[:-1].split("|")
                if len(nag_parts) == 2:
                    nag, time = nag_parts
                    completed = False
                else:
                    nag, time, _ = nag_parts
                    completed = True
                time = parse(time)
            else:
                nag = l
                time = None
                completed = False
            nag = nag.strip()
            if len(nag) == 0:
                continue
            nags.append([nag, time, completed])
    return nags


def save_nags(nags):
    with open(get_naglist(), "w") as nagfile:
        for nag in nags:
            nagfile.write(nag[0])
            if nag[1] is not None:
                nagfile.write("|")
                nagfile.write(nag[1].isoformat())
            if nag[2]:
                nagfile.write("|")
                nagfile.write("Completed")
            nagfile.write("\n")


def create_launchd_script(seconds):
    script = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nagme.donag</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/nagme</string>
    </array>
    <key>StartInterval</key>
    <integer>%d</integer>
    <key>StandardOutPath</key>
    <string>/var/log/nagme.log</string>
    <key>StandardErrorPath</key>
    <string>/var/log/nagme_err.log</string>
</dict>
</plist>""" % seconds
    path = os.path.expanduser("~/Library/LaunchAgents/com.nagme.donag.plist")
    import subprocess
    if os.path.exists(path):
        subprocess.call(["launchctl", "unload", "-w", path])
    with open(path, "w") as plist:
        plist.write(script)
    subprocess.call(["launchctl", "load", "-w", path])
