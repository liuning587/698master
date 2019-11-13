# coding: utf-8
"""metercfg"""
import sys

class MeterCfg():
    def __init__(self):
        self.cfg_no = 2
        self.maddr = '000000000002'
        self.baudrate = 3
        self.ptl = 3
        self.port = 0xF2090201
        self.pwd = ''
        self.rate = 4
        self.usrType = 0
        self.lineMode = 3
        self.stdV = 2200
        self.stdA = 15
        self.collAddr = ''
        self.assetNumber = ''
        self.PT = 1
        self.CT = 1

    def set_cfg_no(self, cfg_no):
        self.cfg_no = cfg_no
        return True

    def set_maddr(self, maddr = '000000000001'):
        self.maddr = "%012d" % int(maddr)
        return True

    def set_baudrate(self, baudrate = 3):
        self.baudrate = baudrate# todo: real baudrate
        return True

    def set_ptl(self, ptl = 2):
        self.ptl = ptl # todo: real ptl
        return True

    def set_port(self, port = 0xF2090201):
        self.port = port #todo: real port oad code
        return True

    def set_pwd(self, pwd = ''):
        if len(pwd) > 0:
            self.pwd = "%012d" % int(pwd)
        else:
            self.pwd = ''
        return True

    def set_rate(self, rate = 4):
        self.rate = rate
        return True

    def set_usrType(self, usrType = 0):
        self.usrType = usrType
        return True

    def set_lineMode(self, lineMode = 1):
        self.lineMode = lineMode
        return True

    def set_stdV(self, stdV = 2200):
        self.stdV = stdV
        return True

    def set_stdA(self, stdA = 15):
        self.stdA = stdA
        return True

    def set_assetNumber(self, assetNumber = ''):
        if len(assetNumber) > 0:
            self.assetNumber = "%012d" % int(assetNumber)
        else:
            self.assetNumber = ''
        return True

    def set_collAddr(self, collAddr = ''):
        if len(collAddr) > 0:
            self.collAddr = "%012d" % int(collAddr)
        else:
            self.collAddr = ''
        return True

    def set_PT(self, PT = 1):
        self.PT = PT
        return True
    
    def set_CT(self, CT = 1):
        self.CT = CT
        return True

    def get_cfg_no(self):
        return '%d' % (self.cfg_no)

    def get_maddr(self):
        return self.maddr

    def get_baudrate(self):
        return {
            0: '300',
            1: '600',
            2: '1200',
            3: '2400',
            4: '4800',
            5: '7200',
            6: '9600',
            7: '19200',
            8: '38400',
            9: '57600',
            10: '115200',
            255: '自适应(255)',
        }.get(self.baudrate, '未知(%d)' % self.baudrate)

    def get_port(self):
        return {
            0xF2010201: '485-1',
            0xF2010202: '485-2',
            0xF2010203: '485-3',
            0xF2090201: 'PLC',
        }.get(self.port, '未知(%08X)' % self.port)

    def get_ptl(self):
        return {
            0: '未知',
            1: '645-1997',
            2: '645-2007',
            3: '698.45',
            4: '188-2004',
        }.get(self.ptl, '无效(%d)' % self.ptl)

    def get_rate(self):
            return '%d' % self.rate

    def get_pwd(self):
        return self.pwd

    def get_lineMode(self):
        return {
            0: '未知',
            1: '单相',
            2: '三相三线',
            3: '三相四线',
        }.get(self.lineMode, '无效(%d)' % self.lineMode)

    def get_usrType(self):
            return '%d' % self.usrType

    def get_stdV(self):
            return '%d' % (self.stdV // 10) + '.%d' % (self.stdV % 10)

    def get_stdA(self):
            return '%d' % (self.stdA // 10) + '.%d' % (self.stdA % 10)

    def get_collAddr(self):
        return self.collAddr

    def get_assetNumber(self):
        return self.assetNumber

    def get_PT(self):
            return '%d' % self.PT

    def get_CT(self):
            return '%d' % self.CT
    
    def get_str_list(self):
        return [
            self.get_cfg_no(),
            self.get_maddr(),
            self.get_baudrate(),
            self.get_port(),
            self.get_ptl(),
            self.get_rate(),
            self.get_pwd(),
            self.get_lineMode(),
            self.get_usrType(),
            self.get_stdV(),
            self.get_stdA(),
            self.get_assetNumber(),
            self.get_collAddr(),
            self.get_PT(),
            self.get_CT(),
        ]
        
    def encode_to_str(self):
        buf = '0204' # 采集档案配置单元:4个成员
        buf += '12%04X' % self.cfg_no # 配置序号
        #
        buf += '020A' # 基本信息:10个成员
        buf += '550705' + self.maddr # 通信地址
        buf += '16%02X' % self.baudrate # 波特率
        buf += '16%02X' % self.ptl # 规约类型
        buf += '51%08X' % self.port # 端口
        
        if len(self.pwd) == 0:
            buf += '0900'
        else:
            buf += '0906' + self.pwd # 通信密码
        buf += '11%02X' % self.rate # 费率个数
        buf += '11%02X' % self.usrType # 用户类型
        buf += '16%02X' % self.lineMode # 接线方式
        buf += '12%04X' % self.stdV # 额定电压
        buf += '12%04X' % self.stdA # 额定电流
        #
        buf += '0204' # 扩展信息:4个成员
        # 采集器地址
        if len(self.collAddr) == 0:
            buf += '5500'
        else:
            buf += '550705' + self.collAddr
        #资产号
        if len(self.assetNumber) == 0:
            buf += '0900'
        else:
            buf += '0906' + self.assetNumber
        buf += '12%04X' % self.PT # PT
        buf += '12%04X' % self.CT # CT
        #
        buf += '0100' #附属属性: 0组
        return buf

    def decode_from_list(self, data):
        # 02 04
        # 12 00 03
        # 02 0A
        #   55 07 05 00 00 00 00 00 03
        #   16 03
        #   16 03
        #   51 F2 01 02 01
        #   09 00
        #   11 04
        #   11 00
        #   16 03
        #   12 00 00
        #   12 00 00
        # 02 04
        #   55 00
        #   09 00
        #   12 00 00
        #   12 00 00
        # 01 00
        
        # 先设置默认值
        cfg_no = 1
        maddr = '000000000001'
        baudrate = 3
        ptl = 3
        port = 0xF2010201
        pwd = ''
        rate = 4
        usrType = 0
        lineMode = 3
        stdV = 2200
        stdA = 15
        collAddr = ''
        assetNumber = ''
        PT = 1
        CT = 1

        offset = 0
        if data[offset] != '02' or data[offset + 1] != '04' or data[offset + 2] != '12':
            return -1
        offset += 3
        cfg_no = int(data[offset] + data[offset + 1], 16)
        offset += 2
        if data[offset] != '02' or data[offset + 1] != '0A':
            return -sys._getframe().f_lineno
        offset += 2

        #TSA
        if data[offset] != '55' or data[offset + 1] != '07' or data[offset + 2] != '05':
            return -sys._getframe().f_lineno
        offset += 3
        maddr = data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5]
        offset += 6

        # baudrate
        if data[offset] != '16':
            return -sys._getframe().f_lineno
        offset += 1
        baudrate = int(data[offset], 16)
        offset += 1

        # ptl
        if data[offset] != '16':
            return -sys._getframe().f_lineno
        offset += 1
        baudrate = int(data[offset], 16)
        offset += 1

        # port
        if data[offset] != '51':
            return -sys._getframe().f_lineno
        offset += 1
        port = int(data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3], 16)
        offset += 4

        # pwd
        if data[offset] != '09':
            return -sys._getframe().f_lineno
        offset += 1
        if data[offset] == '00':
            offset += 1
        elif data[offset] == '06':
            pwd = data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5]
            offset += 6
        else:
            return -sys._getframe().f_lineno

        # rate
        if data[offset] != '11':
            return -sys._getframe().f_lineno
        offset += 1
        rate = int(data[offset], 16)
        offset += 1

        # usrType
        if data[offset] != '11':
            return -sys._getframe().f_lineno
        offset += 1
        usrType = int(data[offset], 16)
        offset += 1

        # lineMode
        if data[offset] != '16':
            return -sys._getframe().f_lineno
        offset += 1
        lineMode = int(data[offset], 16)
        offset += 1

        # stdV
        if data[offset] != '12':
            return -sys._getframe().f_lineno
        offset += 1
        stdV = int(data[offset] + data[offset + 1], 16)
        offset += 2

        # stdA
        if data[offset] != '12':
            return -sys._getframe().f_lineno
        offset += 1
        stdA = int(data[offset] + data[offset + 1], 16)
        offset += 2

        # 扩展信息
        if data[offset] != '02' or data[offset + 1] != '04' or data[offset + 2] != '55':
            return -sys._getframe().f_lineno
        offset += 3

        # collAddr
        if data[offset] == '00':
            offset += 1
        elif data[offset] == '07' and data[offset + 1] == '05':
            offset += 2
            collAddr = data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5]
            offset += 6
        else:
            return -sys._getframe().f_lineno

        # assetNumber
        if data[offset] == '09' and data[offset + 1] == '00': #empty
            offset += 2
        elif data[offset] == '09' and data[offset + 1] == '06':
            offset += 2
            assetNumber = data[offset] + data[offset + 1] + data[offset + 2] + data[offset + 3] + data[offset + 4] + data[offset + 5]
            offset += 6
        else:
            return -sys._getframe().f_lineno

        # PT
        if data[offset] != '12':
            return -sys._getframe().f_lineno
        offset += 1
        PT = int(data[offset] + data[offset + 1], 16)
        offset += 2

        # CT
        if data[offset] != '12':
            return -sys._getframe().f_lineno
        offset += 1
        CT = int(data[offset] + data[offset + 1], 16)
        offset += 2

        # 附属信息 fixme: 暂时只能解析0100
        if data[offset] == '01' and data[offset + 1] == '00':
            offset += 2
        else:
            return -sys._getframe().f_lineno
        
        # 解析成功了
        self.cfg_no = cfg_no
        self.maddr = maddr
        self.baudrate = baudrate
        self.ptl = ptl
        self.port = port
        self.pwd = pwd
        self.rate = rate
        self.usrType = usrType
        self.lineMode = lineMode
        self.stdV = stdV
        self.stdA = stdA
        self.collAddr = collAddr
        self.assetNumber = assetNumber
        self.PT = PT
        self.CT = CT

        return offset


def __text2list(m_text):
    """str to list"""
    m_text = m_text.replace(' ', '').replace('\n', '').upper()  # 处理空格和换行
    # 处理FE前缀
    k = 0
    while m_text[k * 2:(k + 1) * 2] == 'FE':
        k += 1
    m_text = m_text[k * 2:]
    # print('原始报文： ' + m_text + '\n')
    # 写入list
    m_list = []
    for k in range(0, int((len(m_text) + 1) / 2)):
        m_list.append(m_text[k * 2:(k + 1) * 2])
    # if len(m_list) > 0 and len(m_list[-1]) == 1:
    #     m_list[-1] = '0' + m_list[-1]
    if len(m_list) > 0 and len(m_list[-1]) == 1:
        m_list.pop(-1)
    return m_list

if __name__ == "__main__":
    meter = MeterCfg()
    print("meter cfgno:", meter.get_cfg_no())
    print("meter maddr:", meter.get_maddr())
    print("meter apdu:", meter.encode_to_str())
    apdu_text = "0204120003020A5507050000000000031603160351F201020109001104110016031200001200000204550009001200001200000100"
    apdu_list = __text2list(apdu_text)
    print("org       :", apdu_text)
    print("decode:", meter.decode_from_list(apdu_list))
    print("meter apdu:", meter.encode_to_str())
    print("res:", apdu_text == meter.encode_to_str())
