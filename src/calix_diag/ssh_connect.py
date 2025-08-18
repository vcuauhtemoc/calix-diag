import paramiko 
from paramiko_expect import SSHClientInteraction
import sys
import re
from types import SimpleNamespace
from pexpect import pxssh
calix_prompt = r"[A-Za-z]{3}\d{2}\-[A-Za-z]{3}\d{2}\>\s*$"

def jump_connect(jumphost: str,user: str,t_host):
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
    return cx_prompt

def calix_logout(cx_prompt: pxssh.pxssh):
    cx_prompt.sendline("exit")
    return cx_prompt


def run_cmd(cmd:str,interact:pxssh.pxssh) -> str:
    result = ""
    interact.send("\r\n")
    interact.expect(calix_prompt, timeout=10)
    interact.sendline(cmd)
    p_match = interact.expect([calix_prompt,"--MORE--"], timeout=15)
    result += interact.before.decode("utf-8")
    while p_match == 1:
        interact.send(" ")
        p_match = interact.expect([calix_prompt,"--MORE--"], timeout=10)
        result += interact.before.decode("utf-8")
    print("")      
    return result

def pon_port_info(interact:pxssh.pxssh,uid):
    pon_pattern = re.compile(r"PON port\s+:\s+(\d+\/\d+)\s*$",re.MULTILINE)
    detail_output = run_cmd(f"show ont {uid} detail", interact)
    pon: re.Match = pon_pattern.search(detail_output)
    realtime_data = run_cmd(f"show ont on-gpon-port {pon.group(1)} real-time-data",interact)
    print(realtime_data)