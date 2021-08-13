import sys, os
import struct

class apkgFile(object):
    nameLen = 0
    name = ""
    offset = 0
    size = 0

if len(sys.argv) < 2:
    print('usage: feishuapp_unpack.py filename [output_dir]')
    exit()

with open(sys.argv[1], "rb") as f:
    root = os.path.dirname(os.path.realpath(f.name))
    name = os.path.basename(f.name) + '_dir'
    if len(sys.argv) > 2:
        name = sys.argv[2]

    #read header
    firstMark = struct.unpack('>L', f.read(4))[0]
    print('first header mark = {}'.format(firstMark))

    info1 = struct.unpack('<L', f.read(4))[0]
    print('info_version = {}'.format(info1))

    indexInfoLength = struct.unpack('<L', f.read(4))[0]
    print('indexInfoLength = {}'.format(indexInfoLength))

    bodyInfoLength = struct.unpack('<L', f.read(4))[0]
    print('bodyInfoLength = {}'.format(bodyInfoLength))
    '''
    lastMark = struct.unpack('B', f.read(1))[0]
    print('last header mark = {}'.format(lastMark))
    '''
    if firstMark != 0x54504B47 :
        print('its not a feishu_PKG file!!!!!')
        f.close()
        exit()
    '''
    fileCount = struct.unpack('>L', f.read(4))[0]
    print('fileCount = {}'.format(fileCount))
    '''
    print('当前位置'+str(f.tell()))
    #read index
    fileList = []
    
    data = apkgFile()    #第一个文件读取，同时获取hearder截止位置
    data.nameLen = struct.unpack('<L', f.read(4))[0]
    data.name = f.read(data.nameLen)
    data.offset = struct.unpack('<L', f.read(4))[0]
    header_end = data.offset   #hearder截止位置
    data.size = struct.unpack('<L', f.read(4))[0]
    print('readFile = {} at Offset = {}'.format(str(data.name, encoding = "utf-8"), data.offset))
    fileList.append(data)
    while f.tell() < header_end:
        data = apkgFile()
        data.nameLen = struct.unpack('<L', f.read(4))[0]
        data.name = f.read(data.nameLen)
        data.offset = struct.unpack('<L', f.read(4))[0]
        data.size = struct.unpack('<L', f.read(4))[0]
        print('readFile = {} at Offset = {}'.format(str(data.name, encoding = "utf-8"), data.offset))

        fileList.append(data)

    #save files
    for d in fileList:
        
        d.name = '/' + name +'/' +str(d.name, encoding = "utf-8")
        path = root + os.path.dirname(d.name)

        if not os.path.exists(path):
            os.makedirs(path)
        w = open(root + d.name, 'wb')
        f.seek(d.offset)
        w.write(f.read(d.size))
        w.close()

        print('writeFile = {}{}'.format(root, d.name))

    f.close()