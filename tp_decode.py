#!/usr/bin/env python3

import sys


class tp_decoder(object):
    def __init__(self, req_id, res_id, req_name="REQ", res_name="RES"):
        self.frame_names = {req_id: req_name, res_id: res_name}
        self.FRAME_TYPE_MASK = 0xF0
        self.SINGLE_FRAME = 0x00
        self.FIRST_FRAME = 0x10
        self.CONSEQ_FRAME = 0x20
        self.FLOW_CONTROL = 0x30
        self.NO_TP_FRAME = 0xFF
        self.message_buffer = {}
        self.message_lengths = {}
        self.message_status = {}

    def get_frame_type_and_length(self, message):
        first_byte = message.data[0]

        if first_byte & self.FRAME_TYPE_MASK == self.SINGLE_FRAME:
            return self.SINGLE_FRAME, first_byte & 0x0F

        if first_byte & self.FRAME_TYPE_MASK == self.FIRST_FRAME:
            return self.FIRST_FRAME, ((first_byte & 0x0F) << 8) + (message.data[1])

        if first_byte & self.FRAME_TYPE_MASK == self.CONSEQ_FRAME:
            return self.CONSEQ_FRAME, first_byte & 0x0F
        if first_byte & self.FRAME_TYPE_MASK == self.FLOW_CONTROL:
            return self.FLOW_CONTROL, 0

        return self.NO_TP_FRAME, 0

    def get_user_data(self, frame_type, length, message):
        arbitration_id = message.arbitration_id

        if frame_type == self.SINGLE_FRAME:
            return self.frame_names[arbitration_id], message.data[1:length + 1]

        if frame_type == self.FIRST_FRAME:
            self.message_buffer[arbitration_id] = bytearray(message.data[2:])
            self.message_lengths[arbitration_id] = length - 6
            return "", bytearray([])

        if frame_type == self.CONSEQ_FRAME:
            remaining = self.message_lengths.get(arbitration_id)
            if remaining is None:
                sys.stderr.write(
                    "consecutive frame for id {:x} without preceding first frame, skipping\n".format(arbitration_id))
                return "", bytearray([])
            chunk = bytearray(message.data[1:])
            if len(chunk) > remaining:
                chunk = chunk[:remaining]
            self.message_buffer[arbitration_id].extend(chunk)
            remaining -= len(chunk)
            if remaining <= 0:
                self.message_lengths.pop(arbitration_id, None)
                completed = self.message_buffer.pop(arbitration_id)
                return self.frame_names[arbitration_id], completed
            self.message_lengths[arbitration_id] = remaining
            return "", bytearray([])

        if frame_type == self.FLOW_CONTROL:
            flow_status = message.data[0] & 0x0F
            if flow_status == 0:
                flow_status = "Clear To Send"
            elif flow_status == 1:
                flow_status = "Wait"
            elif flow_status == 2:
                flow_status = "Overflow"

            blocksize = message.data[1]
            st_min = message.data[2]
            self.message_status[arbitration_id] = {"flow_status": flow_status, "blocksize": blocksize, "st_min": st_min}
            return "", bytearray([])

        raise ValueError("unknown frame type " + str(frame_type))

    def decode(self, message):
        if message.arbitration_id in self.frame_names:
            frame_type, length = self.get_frame_type_and_length(message)
            return self.get_user_data(frame_type, length, message)
        return "", bytearray([])
