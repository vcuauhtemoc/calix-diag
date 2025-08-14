import argparse
import pathlib as pl
from .ssh_connect import jump_connect_2,calix_login,run_cmd
import time

def main(argv=None):
    ssh_conf_path = f"{pl.Path.home()}/.ssh/config"
    key_path = f"{pl.Path.home()}/.ssh/id_ed25519"
    if not pl.Path(key_path).is_file():
        key_path = f"{pl.Path.home()}/.ssh/id_rsa"
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="Your jumphost username")
    parser.add_argument("olthostname", help="OLT hostname")
    parser.add_argument("uid", help="ONT UID")
    args = parser.parse_args()
    hostname = args.olthostname
    uid = args.uid
    user = args.user
    diag_cmds = [
        f"show ont {uid}",
        f"show ont {uid} detail",
        f"show ont {uid} summary",
        f"show pm ont {uid} 1-day current",
        f"show pm ont-port {uid}/g1 1-day current",
        f"show mac on-ont-port {uid}",
        f"show lldp neighbor",
        f"show log alarm"
    ]
    jump_connect_2("jump-jfk01.as46450.net",user,hostname)
    # jumphost = jump_connect(key_path,"jump-jfk01.as46450.net",user)
    # ssh_interact = calix_login(jumphost,hostname)
    # for e in diag_cmds:
    #     run_cmd(e,ssh_interact)


if __name__ == "__main__":
    raise SystemExit(main())