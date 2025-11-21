import re
from contextlib import contextmanager
from pexpect import pxssh,TIMEOUT
import pexpect
import logging

JUMP_PROMPT = r"[>$#]\s*$" 
CALIX_PROMPT = r"[A-Za-z]{3}\d+(?:\-|\.)[A-Za-z]{3}\d{2}\>\s*$"
PAGER = r"--MORE--"
HOSTKEY_CHECK = "Are you sure you want to continue connecting (yes/no)?"

log = logging.getLogger(__name__)

@contextmanager
def jump_session(jumphost: str,user: str):
    log.debug(f"logging into jumphost...")
    s = pxssh.pxssh()
    s.login(jumphost,user,ssh_key=True)
    try:
        log.debug("Success")
        yield s
    finally:
        log.debug("Logging out of OLT...")
        for _ in range(3):
            s.sendline("")  
            idx = s.expect([JUMP_PROMPT, CALIX_PROMPT, PAGER], timeout=5)
            if idx == 0:      # At jumphost prompt
                log.debug("logged out.")
                break
            if idx == 1:     
                s.sendline("exit")
            if idx == 2:
                s.send("q")
            else:
                s.sendline("exit")


@contextmanager
def calix_session(cx_prompt: pexpect.spawn,t_host: str,is_jump = False):
    log.debug(f"logging into {t_host}...")
    cx_prompt.sendline(f"logmein {t_host}\n")
    session = cx_prompt.expect([CALIX_PROMPT,HOSTKEY_CHECK],timeout=5)
    if session == 1:
        cx_prompt.sendline("yes")
    if session is None:
        raise RuntimeError(f"cannot log into OLT {t_host}.")
    try:
        yield cx_prompt
        log.debug("Success")
    finally:
        log.debug("Exiting OLT session")
        for _ in range(3):
            cx_prompt.sendline("exit")
            idx = cx_prompt.expect([JUMP_PROMPT, CALIX_PROMPT, PAGER], timeout=3)
            if idx == 0:
                break
            if idx == 2:
                cx_prompt.send(" ")

def run_cmd(cmd:str,interact:pexpect.spawn,cmd_timeout=10) -> str:
    result = ""
    interact.send("\r\n")
    is_prompt = interact.expect(CALIX_PROMPT, timeout=10)
    if is_prompt is None:
        raise TimeoutError("CLI not responding")
    interact.sendline(cmd)
    log.debug(f"Running command '{cmd}'")
    result += interact.before.decode("utf-8")
    while True:
        p_match = interact.expect([CALIX_PROMPT,"--MORE--"], timeout=cmd_timeout)
        result += interact.before.decode("utf-8")
        if p_match == 0:
            break
        if p_match == 1:
            interact.send(" ")
        if p_match == 2:
            raise TimeoutError(f"Timed out while running {cmd}")
        # else:
        #     raise Exception(f"command failed: {cmd}")
    return result


def pon_port_info(interact:pexpect.spawn,uid):
    pon_pattern = re.compile(r"PON port\s+:\s+(\d+\/\d+)\s*$",re.MULTILINE)
    detail_output = run_cmd(f"show ont {uid} detail", interact)
    log.debug(f"ONU detail output: {detail_output}")
    pon = pon_pattern.search(detail_output)
    if pon is None: 
        raise ValueError(f"PON port not found in output for uid={uid}")
    return run_cmd(f"show ont on-gpon-port {pon.group(1)} real-time-data",interact,cmd_timeout=20)

def tech_support(interact:pexpect.spawn,uid):
    diag_cmds = [
        f"show ont {uid}",
        f"show ont {uid} detail",
        f"show ont {uid} summary",
        f"show pm ont {uid} 1-day current",
        f"show ont-port {uid}/g1",
        f"show pm ont-port {uid}/g1 1-day current",
        f"show mac on-ont-port {uid}",
        f"show log alarm"
    ]
    for cmd in diag_cmds:
        print(run_cmd(cmd,interact))
        log.debug(f"exited run_cmd() for {cmd}.")
    print(pon_port_info(interact,uid))
    return None
