import sys

import can

import tp_decode
import uds_decode


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else "some.asc"
    req_id = 0x17FC00aa
    res_id = 0x17FE00aa

    my_decoder = tp_decode.tp_decoder(req_id, res_id)
    reader = can.ASCReader(log_file)

    for msg in reader:
        direction, decoded = my_decoder.decode(msg)
        if len(decoded) > 0:
            print(direction + ": " + uds_decode.decode_uds(decoded) + "\t\t[" + " ".join([hex(i) for i in decoded]) + "]")


if __name__ == "__main__":
    main()
