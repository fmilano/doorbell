# Listens for the doorbell event in the Amcrest AD110
# Based on:
# https://github.com/tchellomello/python-amcrest
# https://github.com/tchellomello/python-amcrest/issues/137


from datetime import datetime
import sys
import time

from amcrest import Http, AmcrestError, CommError

import ring_grundig_doorbell

def parse_lines(ret):
    line = ''
    for char in ret.iter_content(decode_unicode=True):
        line = line + char
        if line.endswith('\r\n'):
            yield line.strip()
            line = ''

def main():
    if len(sys.argv) != 5:
        print(sys.argv[0] + ' host port user password')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
    pswd = sys.argv[4]

    ring_grundig_doorbell.init()

    cam = Http(host, port, user, pswd, retries_connection=1, timeout_protocol=3.05)

    while True:
        try:
            ret = cam.command(
                'eventManager.cgi?action=attach&codes=[_DoTalkAction_]',
                timeout_cmd=(3.05, None), stream=True)
            ret.encoding = 'utf-8'


            for line in parse_lines(ret):
                if "Invite" in line:
                    print(datetime.now().replace(microsecond=0),' - Doorbell Button Pressed')
                    ring_grundig_doorbell.ring()
        
        except CommError as error:
            print("CommError: %r", error)
            time.sleep(5)
        except AmcrestError as error:
            print("Error while processing doorbell events: %r", error)
        except KeyboardInterrupt:
            ret.close()
            print(' Done!')
            break
        except:
            print("Unknown exception received. Retrying.")

    ring_grundig_doorbell.term()

if __name__ == '__main__':
    main()
