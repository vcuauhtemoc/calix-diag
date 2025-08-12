import paramiko 
from paramiko_expect import SSHClientInteraction
import time
import typing
import re

def connect(k_path,jumphost,t_host: str,user,ont):
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
    prompt = r"[A-z]{3}\d{2}\-[A-z]{3}\d{2}\>"
    interact = SSHClientInteraction(jump_client,timeout=10,display=True)
    interact.send(f"logmein {t_host}\n")
    interact.expect(prompt, timeout=10)
    if interact.last_match:
        print(f"logged into {t_host}.")
        cmd_output = ""
        for e in diag_cmds:
            interact.send(e)
            interact.expect(prompt,timeout=5)
            cmd_output += interact.current_output_clean
        print(cmd_output)
    interact.close()
    jump_client.close()

def connect_2(k_path: str,jumphost: str,user: str) -> paramiko.SSHClient:
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
    return jump_client

def calix_diag(ssh_client: paramiko.SSHClient,ont: str):
    cmds = [
        f"show ont {ont}\n",
        f"show ont {ont} detail\n ",
        f"show ont {ont} summary\n ",
        f"show pm ont {ont} 1-day current\n",
        f"show pm ont-port {ont}/g1 1-day current\n ",
        f"show mac on-ont-port {ont}\n",
        f"show lldp neighbor\n  "
    ]
    pass