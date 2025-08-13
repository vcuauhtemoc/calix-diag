import paramiko 
from paramiko_expect import SSHClientInteraction

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

def calix_login(jc,t_host):
    prompt = r"[A-z]{3}\d{2}\-[A-z]{3}\d{2}\>"
    interact = SSHClientInteraction(jc,timeout=10,display=True)
    interact.send(f"logmein {t_host}\n")
    interact.expect(prompt,timeout=10)
    print(f"\nLogged into {t_host}.\n")
    return interact

def run_cmd(cmd:str,interact:SSHClientInteraction):
    prompt = r"[A-z]{3}\d{2}\-[A-z]{3}\d{2}\>"
    interact.send(cmd)
    interact.expect([prompt,"--MORE--"], timeout=10)
    while interact.last_match == "--MORE--":
        interact.send(" ")
        interact.expect([prompt,"--MORE--"], timeout=10)
    return None