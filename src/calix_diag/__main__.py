import argparse
import pathlib as pl
from .ssh_connect import jump_session,calix_session,run_cmd,pon_port_info
import logging

logging.basicConfig(
    level=logging.DEBUG,
)

def main(argv=None):

    key_path = f"{pl.Path.home()}/.ssh/id_ed25519"
    if not pl.Path(key_path).is_file():
        key_path = f"{pl.Path.home()}/.ssh/id_rsa"
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="Your jumphost username")
    parser.add_argument("olthostname", help="OLT hostname")
    parser.add_argument("-c", "--cmd",help="command to execute on OLT")
    parser.add_argument("-g", "--get-gpon", help="get gpon port info for ONU")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
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
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    with jump_session("jump-jfk01.as46450.net",user) as jumphost:
        with calix_session(jumphost,hostname) as s:
            if args.get_gpon:
                print(pon_port_info(s,uid))
            if args.cmd:
                print(run_cmd(cmd,s))


if __name__ == "__main__":
    raise SystemExit(main())