import argparse
import pathlib as pl
from .ssh_connect import connect

def main(argv=None):
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
    connect(key_path,"jump-jfk01.as46450.net",hostname,user,uid)

if __name__ == "__main__":
    raise SystemExit(main())