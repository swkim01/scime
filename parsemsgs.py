#!/usr/bin/env python2
from __future__ import with_statement
import sys, os
from struct import unpack, pack
import dcl

# dir with GK1 installed
#kq1vga : SCI01
#kq4vga : SCI0
#ecoquest1,longbow,kq5,kq6 : SCI1
#kq5 : SCI1 (e7 13 00 00 00 00 ...)
#gk2 : SCI2

def parse_map(filemap, step=6):
    '''
    parse message map file
    '''
    resources = []
    try:
        with open(filemap, 'rb') as file:
            map = file.read()
            #print("{:02x} {:02x} {:02x} {}".format(ord(map[0]),ord(map[1]),ord(map[2]),ord(map[1])<<8+ord(map[2])))

            file.seek(0, 0)
            # parse resource type, offset
            while True:
                rtype = file.read(1)
                roffset = int.from_bytes(file.read(2), "little")
                resources.append([rtype, roffset])
                if rtype == b'\xff':
                    break

        rtype = unpack('<B',resources[0][0])[0]
        start = resources[0][1]
        end = resources[1][1]
        count = int((end - start)/step)

        if step == 5:
            return (rtype, {fields[0]: fields[1]<<1 for fields in (unpack('<HI', map[n:n+5]+b'\x00')
                        for n in range(start, end, 5))})
        else:
            return (rtype, {fields[0]: fields[1] for fields in (unpack('<HI', map[n:n+6])
                        for n in range(start, end, 6))})
    except:
        return (None, None)

def read_mheader(file):
    mid = int.from_bytes(file.read(2), "little")
    mpackedsize = int.from_bytes(file.read(2), "little")
    munpackedsize = int.from_bytes(file.read(2), "little")
    mcompress = int.from_bytes(file.read(2), "little")
    return mid, mpackedsize, munpackedsize, mcompress

def parse_mheader(file, offset, patchflag=True):
    file.seek(offset, 0)
    mtype = file.read(1)

    if ord(mtype) & 0xF != 0xF and ord(mtype) & 0xF != 0x3: # if mtype != b'\x0f':
        print("This file is not a message resource!")
        sys.exit(1)
    if ord(mtype) & 0xF == 0xF : # message
        if patchflag == True: # case: patched msg file
            mid, mpackedsize, munpackedsize, mcompress = read_mheader(file)
        else:                # case: original msg files
            dummy = file.read(1)
            mid = int(os.path.basename(file.name).split('.')[0])
            mpackedsize = munpackedsize = mcompress = 0
    else: # text
        if patchflag == True: # case: patched msg file
            mid, mpackedsize, munpackedsize, mcompress = read_mheader(file)
        else:                # case: original msg files
            dummy = file.read(1)
            mid = int(os.path.basename(file.name).split('.')[0])
            mpackedsize = munpackedsize = mcompress = 0

    return [mtype, mid, mpackedsize, munpackedsize, mcompress]

def parse_mheadertail(stream, mheader, patchflag=True):
    mtype = mheader[0]
    if ord(mtype) & 0xF == 0xF : # message
        # remainder read
        # read message header: v3: 10B, v4: 12B
        total = stream.read(4)
        version = (int.from_bytes(total, "little")&0xFFFF)//1000
        #print('ver=', version)
        if version == 3: # v3: 15B
            size = stream.read(2)
            header = total + size
        else:
        #elif version >= 4 and version <= 5: # v4: 15B
            dummy = stream.read(2)
            size = stream.read(2)
            header = total + dummy + size
        count = int.from_bytes(stream.read(2), "little")
        if patchflag == False: # case: msg file
            mheader[2] = mheader[3] = int.from_bytes(size, "little") + 15
        return [header, count]
    else: # text
        return [0, 1]

def parse_mrecord(stream, offset, count, version=4):
    mrecord=[]
    stream.seek(offset, 0)
    # message reader v3: record(10B): noun(1),verb(1),cond(1),seq(1),Talker(1),pos(2, realpos=offset+7(headerlen)+pos),remainder(3)
    # message reader v4: record(11B): noun(1),verb(1),cond(1),seq(1),Talker(1),pos(2, realpos=offset+9(headerlen)+pos),remainder(4)
    for n in range(count):
        noun = stream.read(1)
        verb = stream.read(1)
        cond = stream.read(1)
        seq = stream.read(1)
        talker = stream.read(1)
        if version == 3:
            pos = offset - 8 + int.from_bytes(stream.read(2), "little")
            remainder = int.from_bytes(stream.read(3), "little")
        else:
            pos = offset - 10 + int.from_bytes(stream.read(2), "little")
            remainder = int.from_bytes(stream.read(4), "little")
        mrecord.append([noun, verb, cond, seq, talker, pos, remainder])
    return mrecord

def parse_mtext(file, offset, length):
    # text
    file.seek(offset, 0)
    index = 0
    start = offset
    mrecord = []
    for i in range(length):
        d = file.read(1)
        if d == b'\x00':
            mrecord.append([index, 0, 0, 0, 0, start, 0])
            start = offset + i + 1
            index += 1
        elif d == b'': # end of file
            mrecord.append([index, 0, 0, 0, 0, start, 0])
    return mrecord

def readString(file):
    chars = []
    while True:
        c = file.read(1)
        if c == b'\x00':
            return b''.join(chars)
        chars.append(c)

def try_decode_str(bs, encodings):
    for j, encoding in enumerate(encodings):
        try:
            msg = bs.decode(encoding)
        except:
            if j < len(encodings)-1:
                continue
            msg = bs
        break
    return msg

def try_encode_str(s, encodings):
    for j, encoding in enumerate(encodings):
        try:
            bs = s.encode(encoding)
        except:
            if j < len(encodings)-1:
                continue
            bs = s
        break
    return bs

def parse_messages(file, mrecord, encodings=['latin-1']):
    for i, r in enumerate(mrecord):
        file.seek(r[5], 0) # skip pos
        chars = readString(file)
        #mrecord[i].append(chars.decode('cp949').encode('utf-8'))
        msg = try_decode_str(chars, encodings)
        mrecord[i].append(msg)

def get_msgs_withkey(filename, name):
    messages = {}
    try:
        with open(filename, 'rb') as file:

            # parse message type, offset
            offset = 0
            mheader = parse_mheader(file, offset, patchflag=False)
            mheader = mheader + parse_mheadertail(file, mheader, patchflag=False)
            version = (int.from_bytes(mheader[5], "little")&0xFFFF)//1000
            # message reader v3: header(10B), v4: header{12B)
            if version == 3:
                moffset = offset + 10
            elif version >= 4 and version <= 5:
                moffset = offset + 12
            mrecord = parse_mrecord(file, moffset, mheader[-1], version)
            parse_messages(file, mrecord)
            messages[name] = [mheader, mrecord]

        return messages
    except:
        return None

def get_text_msgs(filename, name):
    messages = {}
    try:
        with open(filename, 'rb') as file:

            # parse message type, offset
            length = os.path.getsize(filename)-2
            offset = 0
            mheader = parse_mheader(file, offset, patchflag=False)
            mheader = mheader + parse_mheadertail(file, mheader, patchflag=False)
            mrecord = parse_mtext(file, offset+2, length)
            parse_messages(file, mrecord)
            messages[name] = [mheader, mrecord]

        return messages
    except:
        return None

def get_msgs_fromdir(msg_dir):
    print("Getting original messages...")

    msg_dirs = os.listdir(msg_dir)
    records = {} #[]
    rtype = None
    for record in sorted(msg_dirs):
        if record.endswith('.msg'): # and record is not 'resource.msg':
            # read record
            name = record.split('.')[0]
            if 'resource' in name or 'RESOURCE' in name:
                continue
            filename = '/'.join((msg_dir, record))
            messages = get_msgs_withkey(filename, name)

            records.update(messages)
            rtype = 0xf

        elif record.endswith('.tex'): # text
            # read text
            name = record.split('.')[0]
            filename = '/'.join((msg_dir, record))
            messages = get_text_msgs(filename, name)

            records.update(messages)
            rtype = 0x3

    if len(records) == 0:
        return (None, None)
    return (rtype, records)

def get_msgs_withmap(filemsg, resmap):
    messages = {}
    try:
        with open(filemsg, 'rb') as file:
            #res = file.read()
            # parse message type, offset
            stream = file
            for key, offset in sorted(resmap.items()):
                mheader = parse_mheader(file, offset)
                moffset = offset + 9

                if mheader[4] >= 16 and mheader[4] <= 18: # dcl compress
                    #print('decompress DCL', mheader[3])
                    stream = dcl.decompress(file, moffset, mheader[3]) # mheader[3] = size
                    moffset = 0 # reset offset
                    stream.seek(0, 0)
                else:
                    stream = file

                # read remainder
                mheader = mheader + parse_mheadertail(stream, mheader)

                if ord(mheader[0])&0xF == 0xF: # message
                    version = (int.from_bytes(mheader[5], "little")&0xFFFF)//1000
                    if version == 3: # v3: header(8B)
                        moffset = moffset + 8
                    else:
                    #elif version >= 4 and version <= 5: # v4: header(10B)
                        moffset = moffset + 10

                    mrecord = parse_mrecord(stream, moffset, mheader[-1], version)
                elif ord(mheader[0])&0xF == 0x3: # text
                    mrecord = parse_mtext(stream, moffset, mheader[2]-6)

                parse_messages(stream, mrecord, encodings=['cp949', 'latin-1'])

                messages[str(key)] = [mheader, mrecord]

        return messages

    except:
        print('Except: get_msgs_withmap')
        return None

def save_map(filename, rtype, resmap):
    print("Saving map...")
    with open(filename, 'wb') as file:
        #default map size = 6
        first = 6
        end = (len(resmap)+1)*6
        file.write(rtype.to_bytes(1, byteorder='little'))
        file.write(first.to_bytes(2, byteorder='little'))
        file.write(0xff.to_bytes(1, byteorder='little'))
        file.write(end.to_bytes(2, byteorder='little'))

        for i, record in enumerate(resmap):
            file.write(record[0].to_bytes(2, byteorder='little'))
            file.write(record[1].to_bytes(4, byteorder='little'))

        file.close()
    print("Saved map OK!")

def update_mapmsg(rtype, resmap, records):
    outmap = {}
    outmsg = {}
    goffset = 0
    sortmap = sorted(resmap.items(), key=(lambda x: int(x[1])))
    for i, (mid, offset) in enumerate(sortmap):
        if str(mid) in records:
            record = records[str(mid)]
            header = record[0]
            msgs = record[1]
            outmap[mid] = goffset

            newrec = []
            newrec.append(header)
            newrec.append([])
            #print("rtype:", rtype)
            if rtype == 0x3:
                moffset = goffset + 9
            else:
                version = (int.from_bytes(header[5], byteorder='little')&0xFFFF)//1000
                if version == 3:
                    moffset = goffset + header[6] * 10 + 17 # v3: fileheader(9B), header(8B), records(10B)
                else:
                    moffset = goffset + header[6] * 11 + 19 # v4: fileheader(9B), header(10B), records(11B)
            for j, msg in enumerate(msgs):
                msg[5] = moffset
                msgbody = try_encode_str(msg[7], encodings=['cp949', 'iso-8859-16', 'iso-8859-1'])
                msgbody += b'\x00'

                moffset += len(msgbody)
                newrec[1].append(msg)

            if rtype == 0x3:
                newrec[0][2] = newrec[0][3] = moffset - goffset - 3
            else:
                newrec[0][2] = newrec[0][3] = moffset - goffset
            outmsg[str(mid)] = newrec
            goffset = moffset

    return (outmap, outmsg)

def save_msg(filename, rtype, sortmap, records):
    print("Saving messages...")
    with open(filename, 'wb') as file:
        count = 0
        for i, (mid, offset) in enumerate(sortmap):
            #res = file.write()
            record = records[str(mid)]
            header = record[0]
            msgs = record[1]

            # save msg file v3: header(9B) & header(8B)
            # save msg file v4: header(9B) & header(10B)
            file.seek(offset, 0)
            file.write(header[0])
            file.write(header[1].to_bytes(2, byteorder='little'))
            file.write(header[2].to_bytes(2, byteorder='little'))
            file.write(header[3].to_bytes(2, byteorder='little'))
            #file.write(header[4].to_bytes(2, byteorder='little'))
            file.write(b'\x00\x00') # no compression

            if rtype == 0xf:
                version = (int.from_bytes(header[5], byteorder='little')&0xFFFF)//1000
                sizebyte = bytearray(header[5])
                if version < 3 or version > 5:
                    sizebyte[0]=160
                    sizebyte[1]=15
                    sizebyte[2]=0
                    sizebyte[3]=0
                file.write(sizebyte) # v3: 6B, v4: 8B
                file.write(header[6].to_bytes(2, byteorder='little'))

                for j, msg in enumerate(msgs):
                    # v3: record(10B): noun(1),verb(1),cond(1),seq(1),Talker(1),pos(2, realpos=offset+9(headerlen)+pos),remainder(3)
                    # v4: record(11B): noun(1),verb(1),cond(1),seq(1),Talker(1),pos(2, realpos=offset+9(headerlen)+pos),remainder(4)
                    file.write(msg[0])
                    file.write(msg[1])
                    file.write(msg[2])
                    file.write(msg[3])
                    file.write(msg[4])
                    file.write((msg[5]-offset-9).to_bytes(2, byteorder='little'))

                    if version == 3:
                        file.write(msg[6].to_bytes(3, byteorder='little'))
                    else:
                        file.write(msg[6].to_bytes(4, byteorder='little'))

            for j, msg in enumerate(msgs):
                offset=msg[5]
                file.seek(offset, 0)
                msgbody = try_encode_str(msg[7], encodings=['cp949', 'iso-8859-16', 'iso-8859-1'])
                msgbody += b'\x00'
                file.write(msgbody)

            file.write(b'\x00')
        # for last i/o access
        for i in range(1024):
            file.write(b'\x00')

        file.close()
    print("Saved messages OK!")

if __name__ == "__main__":
    #load original messages
    gk1_dir = "/mnt/sda/home/urobot/system/game/roms/scummvm/gk1_kor_msg" #(80 28 00 81 c6 13 82 12 16...)
    #records = get_msgs_fromdir(gk1_dir)
    #print(records)

    #load patched messages
    # format: # 6Byte header(SCI1?) = type(f=message), offset(2B, 6=0x0006), type(ff=last entry), offset=size(2B, 468=0x01d4)
    gk1_map = "message.map"  # 0f 06 00 ff d4 01 00 00 00 00 00 00 0f
    filemap = '/'.join((gk1_dir, gk1_map))
    resmap = parse_map(filemap, step=5)
    print(resmap)
    # load messages
    # format: # file offset: messages.map (id 0x0 : 0x0000 ) = 0x0000
    # msg file header(9B): type(f=message), id(2B, 0000), packed size(2B, 3a1e), unpacked size(2B), compress(2B, 0000)
    # msg header(10B): e1 10 00 00 c1 3e c7 00 size(2B, 179=0x00b3)
    # record(11B): noun(23=0x17), verb(68=0x44), cond(0=0x00), seq(1=0x01), Talker(97=0x61) pos(start=0x0+9(header))+0x7bb=0x7c4) 00 00 00 00
    gk1_msg = "resource.msg" # SCI1.1 header(9) 0f 00 00 1e 3a 1e 3a 00 00 msg: e1 10 00 00
    filemsg = '/'.join((gk1_dir, gk1_msg))
    messages = get_msgs_withmap(filemsg, resmap)
    print(messages)

    #resmap, messages = update_mapmsg(resmap, messages)

    #sortmap = sorted(resmap.items(), key=(lambda x: int(x[1])))
    #filemap2 = '/'.join((gk1_dir, "message2.map"))
    #save_map(filemap2, sortmap)
    #filemsg2 = '/'.join((gk1_dir, "resource2.msg"))
    #save_msg(filemsg2, sortmap, messages)
