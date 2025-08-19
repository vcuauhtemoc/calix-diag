import argparse
import pathlib as pl
from .ssh_connect import jump_connect,calix_login,calix_logout,run_cmd,pon_port_info

def main(argv=None):
    key_path = f"{pl.Path.home()}/.ssh/id_ed25519"
    if not pl.Path(key_path).is_file():
        key_path = f"{pl.Path.home()}/.ssh/id_rsa"
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="Your jumphost username")
    parser.add_argument("olthostname", help="OLT hostname")
    parser.add_argument("-c", "--cmd",help="command to execute on OLT")
    parser.add_argument("-g", "--get-gpon", help="get gpon port info for ONU")
    args = parser.parse_args()
    hostname = args.olthostname
    user = args.user
    cmd = args.cmd
    uid = args.get_gpon
    # diag_cmds = [
    #     f"show ont {uid}",
    #     f"show ont {uid} detail",
    #     f"show ont {uid} summary",
    #     f"show pm ont {uid} 1-day current",
    #     f"show pm ont-port {uid}/g1 1-day current",
    #     f"show mac on-ont-port {uid}",
    #     f"show lldp neighbor",
    #     f"show log alarm"
    # ]
    with jump_connect("jump-jfk01.as46450.net",user) as jumphost:
        calix_login(jumphost,hostname)
        try:
            if args.get_gpon:
                pon_port_info(jumphost,uid)
            if args.cmd:
                print(run_cmd(cmd,jumphost))
        finally:
            calix_logout(jumphost)


if __name__ == "__main__":
    raise SystemExit(main())