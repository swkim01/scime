import io

# extracted from scummvm source file (common/dcl.cpp)

length_tree = [
        0x00001002, 0x00003004, 0x00005006, 0x00007008, #0 - 3
        0x0000900a, 0x0000b00c, 0x40000001, 0x0000d00e, #4 - 7
        0x0000f010, 0x00011012, 0x40000003, 0x40000002, #8 - 11
        0x40000000, 0x00013014, 0x00015016, 0x00017018, #12 - 15
        0x40000006, 0x40000005, 0x40000004, 0x0001901a, #16 - 19
        0x0001b01c, 0x4000000a, 0x40000009, 0x40000008, #20 - 23
        0x40000007, 0x0001d01e, 0x4000000d, 0x4000000c, #24 - 27
        0x4000000b, 0x4000000f, 0x4000000e, 0x00000000  #28 - 31
        ]
distance_tree = [
        0x00001002, 0x00003004, 0x00005006, 0x00007008, #0 - 3
        0x0000900a, 0x0000b00c, 0x40000000, 0x0000d00e, #4 - 7
        0x0000f010, 0x00011012, 0x00013014, 0x00015016, #8 - 11
        0x00017018, 0x0001901a, 0x0001b01c, 0x0001d01e, #12 - 15
        0x0001f020, 0x00021022, 0x00023024, 0x00025026, #16 - 19
        0x00027028, 0x0002902a, 0x0002b02c, 0x40000002, #20 - 23
        0x40000001, 0x0002d02e, 0x0002f030, 0x00031032, #24 - 27
        0x00033034, 0x00035036, 0x00037038, 0x0003903a, #28 - 31
        0x0003b03c, 0x0003d03e, 0x0003f040, 0x00041042, #32 - 35
        0x00043044, 0x00045046, 0x00047048, 0x0004904a, #36 - 39
        0x0004b04c, 0x40000006, 0x40000005, 0x40000004, #40 - 43
        0x40000003, 0x0004d04e, 0x0004f050, 0x00051052, #44 - 47
        0x00053054, 0x00055056, 0x00057058, 0x0005905a, #48 - 51
        0x0005b05c, 0x0005d05e, 0x0005f060, 0x00061062, #52 - 55
        0x00063064, 0x00065066, 0x00067068, 0x0006906a, #56 - 59
        0x0006b06c, 0x0006d06e, 0x40000015, 0x40000014, #60 - 63
        0x40000013, 0x40000012, 0x40000011, 0x40000010, #64 - 67
        0x4000000f, 0x4000000e, 0x4000000d, 0x4000000c, #68 - 71
        0x4000000b, 0x4000000a, 0x40000009, 0x40000008, #72 - 75
        0x40000007, 0x0006f070, 0x00071072, 0x00073074, #76 - 79
        0x00075076, 0x00077078, 0x0007907a, 0x0007b07c, #80 - 83
        0x0007d07e, 0x4000002f, 0x4000002e, 0x4000002d, #84 - 87
        0x4000002c, 0x4000002b, 0x4000002a, 0x40000029, #88 - 91
        0x40000028, 0x40000027, 0x40000026, 0x40000025, #92 - 95
        0x40000024, 0x40000023, 0x40000022, 0x40000021, #96 - 99
        0x40000020, 0x4000001f, 0x4000001e, 0x4000001d, #100 - 103
        0x4000001c, 0x4000001b, 0x4000001a, 0x40000019, #104 - 107
        0x40000018, 0x40000017, 0x40000016, 0x4000003f, #108 - 111
        0x4000003e, 0x4000003d, 0x4000003c, 0x4000003b, #112 - 115
        0x4000003a, 0x40000039, 0x40000038, 0x40000037, #116 - 119
        0x40000036, 0x40000035, 0x40000034, 0x40000033, #120 - 123
        0x40000032, 0x40000031, 0x40000030, 0x00000000  #124 - 127
        ]
ascii_tree = [
        0x00001002, 0x00003004, 0x00005006, 0x00007008, #0 - 3
        0x0000900a, 0x0000b00c, 0x0000d00e, 0x0000f010, #4 - 7
        0x00011012, 0x00013014, 0x00015016, 0x00017018, #8 - 11
        0x0001901a, 0x0001b01c, 0x0001d01e, 0x0001f020, #12 - 15
        0x00021022, 0x00023024, 0x00025026, 0x00027028, #16 - 19
        0x0002902a, 0x0002b02c, 0x0002d02e, 0x0002f030, #20 - 23
        0x00031032, 0x00033034, 0x00035036, 0x00037038, #24 - 27
        0x0003903a, 0x0003b03c, 0x40000020, 0x0003d03e, #28 - 31
        0x0003f040, 0x00041042, 0x00043044, 0x00045046, #32 - 35
        0x00047048, 0x0004904a, 0x0004b04c, 0x0004d04e, #36 - 39
        0x0004f050, 0x00051052, 0x00053054, 0x00055056, #40 - 43
        0x00057058, 0x0005905a, 0x0005b05c, 0x0005d05e, #44 - 47
        0x0005f060, 0x00061062, 0x40000075, 0x40000074, #48 - 51
        0x40000073, 0x40000072, 0x4000006f, 0x4000006e, #52 - 55
        0x4000006c, 0x40000069, 0x40000065, 0x40000061, #56 - 59
        0x40000045, 0x00063064, 0x00065066, 0x00067068, #60 - 63
        0x0006906a, 0x0006b06c, 0x0006d06e, 0x0006f070, #64 - 67
        0x00071072, 0x00073074, 0x00075076, 0x00077078, #68 - 71
        0x0007907a, 0x0007b07c, 0x0007d07e, 0x0007f080, #72 - 75
        0x00081082, 0x00083084, 0x00085086, 0x40000070, #76 - 79
        0x4000006d, 0x40000068, 0x40000067, 0x40000066, #80 - 83
        0x40000064, 0x40000063, 0x40000062, 0x40000054, #84 - 87
        0x40000053, 0x40000052, 0x4000004f, 0x4000004e, #88 - 91
        0x4000004c, 0x40000049, 0x40000044, 0x40000043, #92 - 95
        0x40000041, 0x40000031, 0x4000002d, 0x00087088, #96 - 99
        0x0008908a, 0x0008b08c, 0x0008d08e, 0x0008f090, #100 - 103
        0x00091092, 0x00093094, 0x00095096, 0x00097098, #104 - 107
        0x0009909a, 0x0009b09c, 0x0009d09e, 0x0009f0a0, #108 - 111
        0x000a10a2, 0x000a30a4, 0x40000077, 0x4000006b, #112 - 115
        0x40000055, 0x40000050, 0x4000004d, 0x40000046, #116 - 119
        0x40000042, 0x4000003d, 0x40000038, 0x40000037, #120 - 123
        0x40000035, 0x40000034, 0x40000033, 0x40000032, #124 - 127
        0x40000030, 0x4000002e, 0x4000002c, 0x40000029, #128 - 131
        0x40000028, 0x4000000d, 0x4000000a, 0x000a50a6, #132 - 135
        0x000a70a8, 0x000a90aa, 0x000ab0ac, 0x000ad0ae, #136 - 139
        0x000af0b0, 0x000b10b2, 0x000b30b4, 0x000b50b6, #140 - 143
        0x000b70b8, 0x000b90ba, 0x000bb0bc, 0x000bd0be, #144 - 147
        0x000bf0c0, 0x40000079, 0x40000078, 0x40000076, #148 - 151
        0x4000005f, 0x4000005b, 0x40000057, 0x40000048, #152 - 155
        0x40000047, 0x4000003a, 0x40000039, 0x40000036, #156 - 159
        0x4000002f, 0x4000002a, 0x40000027, 0x40000022, #160 - 163
        0x40000009, 0x000c10c2, 0x000c30c4, 0x000c50c6, #164 - 167
        0x000c70c8, 0x000c90ca, 0x000cb0cc, 0x000cd0ce, #168 - 171
        0x000cf0d0, 0x000d10d2, 0x000d30d4, 0x000d50d6, #172 - 175
        0x000d70d8, 0x000d90da, 0x000db0dc, 0x000dd0de, #176 - 179
        0x000df0e0, 0x000e10e2, 0x000e30e4, 0x000e50e6, #180 - 183
        0x000e70e8, 0x000e90ea, 0x4000005d, 0x40000059, #184 - 187
        0x40000058, 0x40000056, 0x4000004b, 0x4000003e, #188 - 191
        0x4000002b, 0x000eb0ec, 0x000ed0ee, 0x000ef0f0, #192 - 195
        0x000f10f2, 0x000f30f4, 0x000f50f6, 0x000f70f8, #196 - 199
        0x000f90fa, 0x000fb0fc, 0x000fd0fe, 0x000ff100, #200 - 203
        0x00101102, 0x00103104, 0x00105106, 0x00107108, #204 - 207
        0x0010910a, 0x0010b10c, 0x0010d10e, 0x0010f110, #208 - 211
        0x00111112, 0x00113114, 0x00115116, 0x00117118, #212 - 215
        0x0011911a, 0x0011b11c, 0x0011d11e, 0x0011f120, #216 - 219
        0x00121122, 0x00123124, 0x00125126, 0x00127128, #220 - 223
        0x0012912a, 0x0012b12c, 0x0012d12e, 0x0012f130, #224 - 227
        0x00131132, 0x00133134, 0x4000007a, 0x40000071, #228 - 231
        0x40000026, 0x40000024, 0x40000021, 0x00135136, #232 - 235
        0x00137138, 0x0013913a, 0x0013b13c, 0x0013d13e, #236 - 239
        0x0013f140, 0x00141142, 0x00143144, 0x00145146, #240 - 243
        0x00147148, 0x0014914a, 0x0014b14c, 0x0014d14e, #244 - 247
        0x0014f150, 0x00151152, 0x00153154, 0x00155156, #248 - 251
        0x00157158, 0x0015915a, 0x0015b15c, 0x0015d15e, #252 - 255
        0x0015f160, 0x00161162, 0x00163164, 0x00165166, #256 - 259
        0x00167168, 0x0016916a, 0x0016b16c, 0x0016d16e, #260 - 263
        0x0016f170, 0x00171172, 0x00173174, 0x00175176, #264 - 267
        0x00177178, 0x0017917a, 0x0017b17c, 0x0017d17e, #268 - 271
        0x0017f180, 0x00181182, 0x00183184, 0x00185186, #272 - 275
        0x00187188, 0x0018918a, 0x0018b18c, 0x0018d18e, #276 - 279
        0x0018f190, 0x00191192, 0x00193194, 0x00195196, #280 - 283
        0x00197198, 0x0019919a, 0x0019b19c, 0x0019d19e, #284 - 287
        0x0019f1a0, 0x001a11a2, 0x001a31a4, 0x001a51a6, #288 - 291
        0x001a71a8, 0x001a91aa, 0x001ab1ac, 0x001ad1ae, #292 - 295
        0x001af1b0, 0x001b11b2, 0x001b31b4, 0x4000007c, #296 - 299
        0x4000007b, 0x4000006a, 0x4000005c, 0x4000005a, #300 - 303
        0x40000051, 0x4000004a, 0x4000003f, 0x4000003c, #304 - 307
        0x40000000, 0x001b51b6, 0x001b71b8, 0x001b91ba, #308 - 311
        0x001bb1bc, 0x001bd1be, 0x001bf1c0, 0x001c11c2, #312 - 315
        0x001c31c4, 0x001c51c6, 0x001c71c8, 0x001c91ca, #316 - 319
        0x001cb1cc, 0x001cd1ce, 0x001cf1d0, 0x001d11d2, #320 - 323
        0x001d31d4, 0x001d51d6, 0x001d71d8, 0x001d91da, #324 - 327
        0x001db1dc, 0x001dd1de, 0x001df1e0, 0x001e11e2, #328 - 331
        0x001e31e4, 0x001e51e6, 0x001e71e8, 0x001e91ea, #332 - 335
        0x001eb1ec, 0x001ed1ee, 0x001ef1f0, 0x001f11f2, #336 - 339
        0x001f31f4, 0x001f51f6, 0x001f71f8, 0x001f91fa, #340 - 343
        0x001fb1fc, 0x001fd1fe, 0x400000f4, 0x400000f3, #344 - 347
        0x400000f2, 0x400000ee, 0x400000e9, 0x400000e5, #348 - 351
        0x400000e1, 0x400000df, 0x400000de, 0x400000dd, #352 - 355
        0x400000dc, 0x400000db, 0x400000da, 0x400000d9, #356 - 359
        0x400000d8, 0x400000d7, 0x400000d6, 0x400000d5, #360 - 363
        0x400000d4, 0x400000d3, 0x400000d2, 0x400000d1, #364 - 367
        0x400000d0, 0x400000cf, 0x400000ce, 0x400000cd, #368 - 371
        0x400000cc, 0x400000cb, 0x400000ca, 0x400000c9, #372 - 375
        0x400000c8, 0x400000c7, 0x400000c6, 0x400000c5, #376 - 379
        0x400000c4, 0x400000c3, 0x400000c2, 0x400000c1, #380 - 383
        0x400000c0, 0x400000bf, 0x400000be, 0x400000bd, #384 - 387
        0x400000bc, 0x400000bb, 0x400000ba, 0x400000b9, #388 - 391
        0x400000b8, 0x400000b7, 0x400000b6, 0x400000b5, #392 - 395
        0x400000b4, 0x400000b3, 0x400000b2, 0x400000b1, #396 - 399
        0x400000b0, 0x4000007f, 0x4000007e, 0x4000007d, #400 - 403
        0x40000060, 0x4000005e, 0x40000040, 0x4000003b, #404 - 407
        0x40000025, 0x40000023, 0x4000001f, 0x4000001e, #408 - 411
        0x4000001d, 0x4000001c, 0x4000001b, 0x40000019, #412 - 415
        0x40000018, 0x40000017, 0x40000016, 0x40000015, #416 - 419
        0x40000014, 0x40000013, 0x40000012, 0x40000011, #420 - 423
        0x40000010, 0x4000000f, 0x4000000e, 0x4000000c, #424 - 427
        0x4000000b, 0x40000008, 0x40000007, 0x40000006, #428 - 431
        0x40000005, 0x40000004, 0x40000003, 0x40000002, #432 - 435
        0x40000001, 0x400000ff, 0x400000fe, 0x400000fd, #436 - 439
        0x400000fc, 0x400000fb, 0x400000fa, 0x400000f9, #440 - 443
        0x400000f8, 0x400000f7, 0x400000f6, 0x400000f5, #444 - 447
        0x400000f1, 0x400000f0, 0x400000ef, 0x400000ed, #448 - 451
        0x400000ec, 0x400000eb, 0x400000ea, 0x400000e8, #452 - 455
        0x400000e7, 0x400000e6, 0x400000e4, 0x400000e3, #456 - 459
        0x400000e2, 0x400000e0, 0x400000af, 0x400000ae, #460 - 463
        0x400000ad, 0x400000ac, 0x400000ab, 0x400000aa, #464 - 467
        0x400000a9, 0x400000a8, 0x400000a7, 0x400000a6, #468 - 471
        0x400000a5, 0x400000a4, 0x400000a3, 0x400000a2, #472 - 475
        0x400000a1, 0x400000a0, 0x4000009f, 0x4000009e, #476 - 479
        0x4000009d, 0x4000009c, 0x4000009b, 0x4000009a, #480 - 483
        0x40000099, 0x40000098, 0x40000097, 0x40000096, #484 - 487
        0x40000095, 0x40000094, 0x40000093, 0x40000092, #488 - 491
        0x40000091, 0x40000090, 0x4000008f, 0x4000008e, #492 - 495
        0x4000008d, 0x4000008c, 0x4000008b, 0x4000008a, #496 - 499
        0x40000089, 0x40000088, 0x40000087, 0x40000086, #500 - 503
        0x40000085, 0x40000084, 0x40000083, 0x40000082, #504 - 507
        0x40000081, 0x40000080, 0x4000001a, 0x00000000  #508 - 511
        ]

DCL_BINARY_MODE = 0
DCL_ASCII_MODE = 1

class DecompressorDCL(object):
    def __init__(self, source, offset):
        self.source = source
        self.source.seek(offset, 0)
        self._nBits = 0
        self._bytesRead = 0
        self._bytesWritten = 0
        self._dwBits = 0

    def fetchBitsLSB(self):
        while self._nBits <= 24:
            data = int.from_bytes(self.source.read(1), 'little')
            self._dwBits = self._dwBits | (data << self._nBits)
            self._nBits = self._nBits + 8
            self._bytesRead = self._bytesRead + 1

    def getBitsLSB(self, n):
        if self._nBits < n:
            self.fetchBitsLSB()
        ret = self._dwBits & ~((~0) << n)
        self._dwBits = self._dwBits >> n
        self._nBits = self._nBits - n
        return ret

    def getByteLSB(self):
        return self.getBitsLSB(8)

    def putByte(self, data):
        self.dest.write(data.to_bytes(1, byteorder='little'))
        self._bytesWritten = self._bytesWritten + 1

    def huffman_lookup(self, tree):
        pos = 0
        while (tree[pos] & 0x40000000) == 0:
            bit = self.getBitsLSB(1)
            #print(pos, ":", bit)
            if bit:
                pos = tree[pos] & 0xFFF
            else:
                pos = tree[pos] >> 12
        #print("=", tree[pos] & 0xFFFF)
        return tree[pos] & 0xFFFF

    def unpack(self, target, targetSize, targetFixedSize):
        dictionary = bytearray(4096)
        dictPos = 0
        dictSize = 0
        tokenOffset = 0
        tokenLength = 0

        self.dest = target
        mode = self.getByteLSB()
        dictType = self.getByteLSB()
        if dictType < 4 or dictType > 6:
            print("Error: unsupported dict type ", dictType)
            return False

        dictSize = 1 << (dictType + 6)
        dictMask = dictSize - 1
        try:
          while not targetFixedSize or self._bytesWritten < targetSize:
            if self.getBitsLSB(1) != 0: # (length,distance) pair
                #print('length,distance pair')
                value = self.huffman_lookup(length_tree)
                if value < 8:
                    tokenLength = value + 2
                else:
                    tokenLength = 8 + (1 << (value - 7)) + self.getBitsLSB(value - 7)
                if tokenLength == 519:
                    break # End of stream signal

                value = self.huffman_lookup(distance_tree)
                if tokenLength == 2:
                    tokenOffset = (value << 2) | self.getBitsLSB(2)
                else:
                    tokenOffset = (value<<dictType) | self.getBitsLSB(dictType)
                tokenOffset = tokenOffset + 1

                if targetFixedSize:
                    if (tokenLength + self._bytesWritten > targetSize):
                        print("Error: Write out of bounds")
                        return False
                if self._bytesWritten < tokenOffset:
                    print("Error: Attempt to copy from before beginning inputstream")
                    return False

                dictBaseIndex = (dictPos - tokenOffset) & dictMask
                dictIndex = dictBaseIndex
                dictNextIndex = dictPos

                while tokenLength:
                    self.putByte(dictionary[dictIndex])
                    dictionary[dictNextIndex] = dictionary[dictIndex]
                    dictNextIndex = (dictNextIndex + 1) & dictMask
                    dictIndex = (dictIndex + 1) & dictMask
                    if dictIndex == dictPos:
                        dictIndex = dictBaseIndex
                    if dictNextIndex == dictSize:
                        dictNextIndex = 0
                    tokenLength = tokenLength - 1
                dictPos = dictNextIndex

            else: # Copy byte verbatim
                #print('copy byte verbatim')
                if mode == DCL_ASCII_MODE:
                    value = self.huffman_lookup(ascii_tree)
                else:
                    value = self.getByteLSB()
                self.putByte(value)

                dictionary[dictPos] = value & 0xFF
                dictPos = dictPos + 1
                if dictPos >= dictSize:
                    dictPos = 0

          if targetFixedSize:
            if self._bytesWritten != targetSize:
                print("Error: Inconsistent bytes written", self._bytesWritten, targetSize)
                return self._bytesWritten == targetSize
        except:
            print("Error: unpack error", self._bytesWritten, targetSize)
            pass

        #print('bytesWritten=', self._bytesWritten)
        return True

def decompress(source, offset, size):
    #print('create DCL object')
    dclobject = DecompressorDCL(source, offset)
    target = io.BytesIO()
    #print('unpack')
    dclobject.unpack(target, size, True)
    #print('unpack success')
    return target
