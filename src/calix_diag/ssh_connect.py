import paramiko 
import time
import re

def connect(k_path,jumphost,t_host,user,ont):
    diag_cmds = [
        f"show ont {ont}\n",
        f"show ont {ont} detail\n ",
        f"show ont {ont} summary\n ",
        f"show pm ont {ont} 1-day current\n",
        f"show pm ont-port {ont}/g1 1-day current\n ",
        f"show mac on-ont-port {ont}\n",
        f"show lldp neighbor\n  "
    ]
    if "25519" in k_path:
        ssh_key = paramiko.Ed25519Key(filename=k_path)
    else:
        ssh_key = paramiko.RSAKey(filename=k_path)
    jump_client = paramiko.SSHClient()
    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jump_client.connect(
        hostname=jumphost,
        username=user,
        pkey=ssh_key
    )
    channel = jump_client.invoke_shell()
    time.sleep(1)
    if channel.recv_ready():
        channel.send(f"logmein {t_host}\n")
    time.sleep(5)
    stdout = channel.recv(65535).decode(errors="ignore")
    stdout = stdout.splitlines()
    prompt = stdout[len(stdout) - 1]
        
    if re.match(r"[A-z]{3}\d{2}\-[A-z]{3}\d{2}\>",str(prompt)):
        cmd_output = ""
        for e in diag_cmds:
            channel.send(e)
            time.sleep(2)
            cmd_output += channel.recv(65535).decode(errors="ignore")
            time.sleep(1)
        print(cmd_output)

    channel.close()
    jump_client.close()