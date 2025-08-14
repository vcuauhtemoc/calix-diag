import paramiko 
from paramiko_expect import SSHClientInteraction
import sys
from pexpect import pxssh
prompt = r"[A-Za-z]{3}\d{2}\-[A-Za-z]{3}\d{2}\>\s*$"

def jump_connect(k_path: str,jumphost: str,user: str) -> paramiko.SSHClient:
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

def jump_connect_2(jumphost: str,user: str,t_host):
    jump_client = pxssh.pxssh()
    jump_client.login(jumphost,user,ssh_key=True)
    print(str(jump_client.after))
    jump_client.sendline(f"logmein {t_host}")
    jump_client.prompt()
    print(str(jump_client.before))
    jump_client.sendline("exit")
    jump_client.prompt()
    print(str(jump_client.before))
    jump_client.logout()

def calix_login(jc,t_host):
    interact = SSHClientInteraction(jc,timeout=10,display=True)
    interact.send(f"logmein {t_host}\n")
    interact.expect(prompt,timeout=10)
    print(f"\nLogged into {t_host}.\n")
    return interact

def run_cmd(cmd:str,interact:SSHClientInteraction):
    interact.send(cmd,newline="\r\n")
    interact.expect([prompt,"--MORE--"], timeout=10)
    print(interact.current_output.splitlines()[len(interact.current_output.splitlines()) - 1])
    print("* * *")
    while interact.last_match == "--MORE--":
        interact.send(" ")
        interact.expect([prompt,"--MORE--"], timeout=10)
    return None