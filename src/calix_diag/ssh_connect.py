import paramiko 
from paramiko_expect import SSHClientInteraction
import sys
from types import SimpleNamespace
from pexpect import pxssh
calix_prompt = r"[A-Za-z]{3}\d{2}\-[A-Za-z]{3}\d{2}\>\s*$"

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
    try:
        jump_client.login(jumphost,user,ssh_key=True)
        return jump_client
    except Exception as ex: # turn this into raise
        jump_client.logout()
        for e in ex.args:
            print(e)
        
        

def calix_login(cx_prompt: pxssh.pxssh,t_host):
    cx_prompt.sendline(f"logmein {t_host}\n")
    cx_prompt.expect(calix_prompt,timeout=5)
    print(f"\nLogged into {t_host}.\n")
    return cx_prompt

def calix_logout(cx_prompt: pxssh.pxssh):
    cx_prompt.sendline("exit")
    return cx_prompt


def run_cmd(cmd:str,interact:pxssh.pxssh):
    interact.sendline(cmd)
    p_match = interact.expect([calix_prompt,r"\r\n"], timeout=10)
    print(interact.before.decode("utf-8"))
    while p_match == 1:
        interact.send(" ")
        print(interact.before.decode("utf-8"))        
        interact.expect([calix_prompt,"\r\n"], timeout=10)
    return None