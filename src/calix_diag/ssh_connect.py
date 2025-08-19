import re
from contextlib import contextmanager
from pexpect import pxssh
import logging

JUMP_PROMPT = r"[>$#]\s*$" 
CALIX_PROMPT = r"[A-Za-z]{3}\d{2}\-[A-Za-z]{3}\d{2}\>\s*$"
PAGER = r"--MORE--"

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
            s.sendline("")  # nudge; flush any pager/prompt debris
            idx = s.expect([JUMP_PROMPT, CALIX_PROMPT, PAGER], timeout=3)
            if idx == 0:      # At jumphost prompt
                log.debug("logged out.")
                break
            if idx == 1:      # Still at Calix prompt → send exit
                s.sendline("exit")
            elif idx == 2:    # Pager → advance
                s.send("q")
            else:
                s.sendline("exit")

@contextmanager
def calix_session(cx_prompt: pxssh.pxssh,t_host: str):
    log.debug(f"logging into {t_host}...")
    cx_prompt.sendline(f"logmein {t_host}\n")
    session = cx_prompt.expect(CALIX_PROMPT,timeout=5)
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
        # Final attempt to sync on jumphost prompt

def run_cmd(cmd:str,interact:pxssh.pxssh,timeout=10) -> str:
    result = ""
    interact.send("\r\n")
    is_prompt = interact.expect(CALIX_PROMPT, timeout=10)
    if is_prompt is None:
        raise TimeoutError("CLI not responding")
    interact.sendline(cmd)
    log.debug(f"Running command '{cmd}'")
    result += interact.before.decode("utf-8")
    while True:
        p_match = interact.expect([CALIX_PROMPT,"--MORE--"], timeout=timeout)
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
    pon = pon_pattern.search(detail_output)
    if pon is None: 
        raise ValueError(f"PON port not found in output for uid={uid}")
    return run_cmd(f"show ont on-gpon-port {pon.group(1)} real-time-data",interact,timeout=20)
    