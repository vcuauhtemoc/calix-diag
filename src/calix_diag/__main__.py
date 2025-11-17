import argparse
import pathlib as pl
import logging
import pexpect
from socket import gethostname
from .ssh_connect import *
logging.basicConfig(
    level=logging.DEBUG,
)

def main(argv=None):
    p = pl.Path('.')
    key_path = f"{pl.Path.home()}/.ssh/id_ed25519"
    if not pl.Path(key_path).is_file():
        key_path = f"{pl.Path.home()}/.ssh/id_rsa"
    parser = argparse.ArgumentParser()
    parser.add_argument("olthostname", help="OLT hostname")
    parser.add_argument("-u", "--user", help="Your jumphost username",required=False)
    parser.add_argument("-c", "--cmd",help="command to execute on OLT")
    parser.add_argument("-t", "--tech-support", help="get ONU/OLT info for standard trobleshooting",metavar="UID")
    parser.add_argument("-g", "--get-gpon", help="get gpon port info for ONU",metavar="UID")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    olt = args.olthostname
    user = args.user
    cmd = args.cmd
    g_uid = args.get_gpon
    t_uid = args.tech_support
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
    hostname = gethostname()

    if hostname == "jump-jfk01.as46450.net":
        jumphost = pexpect.spawn("/bin/bash")
        with calix_session(jumphost,olt) as s:
            if args.get_gpon:
                print(pon_port_info(s,g_uid))
            if args.cmd:
                print(run_cmd(cmd,s))
            if args.tech_support:
                tech_support(s,t_uid)
        # potentially allow this to be run directly in the jumphost.
        # would require reworking the functions to not use pxssh
    else:
        with jump_session("jump-jfk01.as46450.net",user) as jumphost:
            with calix_session(jumphost,olt) as s:
                if args.get_gpon:
                    print(pon_port_info(s,g_uid))
                if args.cmd:
                    print(run_cmd(cmd,s))
                if args.tech_support:
                    tech_support(s,t_uid)



if __name__ == "__main__":
    raise SystemExit(main())