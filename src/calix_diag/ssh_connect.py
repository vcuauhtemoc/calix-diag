import re
from contextlib import contextmanager
from pexpect import pxssh
import logging

calix_prompt = r"[A-Za-z]{3}\d{2}\-[A-Za-z]{3}\d{2}\>\s*$"
log = logging.getLogger(__name__)

@contextmanager
def jump_connect(jumphost: str,user: str):
    log.debug(f"logging into jumphost...")
    jump_client = pxssh.pxssh()
    try:
        jump_client.login(jumphost,user,ssh_key=True)
        # log.debug(jump_client.before.decode("utf-8"))
        log.debug("Success")
        yield jump_client
    finally:
        log.debug("Logging out of jumphost...")
        try:
            jump_client.sendline("exit") # to back out of OLT first
            jump_client.prompt()
            jump_client.logout()
            log.debug("Success")
        except Exception as e:
            log.debug(f"Error while logging out: {e}")

        
def calix_login(cx_prompt: pxssh.pxssh,t_host: str):
    log.debug(f"logging into {t_host}...")
    cx_prompt.sendline(f"logmein {t_host}\n")
    session = cx_prompt.expect(calix_prompt,timeout=5)
    if session is None:
        raise RuntimeError(f"cannot log into OLT {t_host}.")
    log.debug("Success")
 

def run_cmd(cmd:str,interact:pxssh.pxssh,timeout=10) -> str:
    result = ""
    interact.send("\r\n")
    is_prompt = interact.expect(calix_prompt, timeout=10)
    if is_prompt is None:
        raise TimeoutError("CLI not responding")
    interact.sendline(cmd)
    log.debug(f"Running command '{cmd}'")
    result += interact.before.decode("utf-8")
    while True:
        p_match = interact.expect([calix_prompt,"--MORE--"], timeout=timeout)
        result += interact.before.decode("utf-8")
        if p_match == 0:
            break
        if p_match == 1:
            interact.send(" ")
        else:
            raise TimeoutError(f"Timed out while running {cmd}")
    return result


def pon_port_info(interact:pxssh.pxssh,uid):
    pon_pattern = re.compile(r"PON port\s+:\s+(\d+\/\d+)\s*$",re.MULTILINE)
    detail_output = run_cmd(f"show ont {uid} detail", interact)
    log.debug(f"ONU detail output: {detail_output}")
    # pon = pon_pattern.search(detail_output)
    # if pon is None: 
    #     raise ValueError(f"PON port not found in output for uid={uid}")
    # return run_cmd(f"show ont on-gpon-port {pon.group(1)} real-time-data",interact,timeout=20)
    