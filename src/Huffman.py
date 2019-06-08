# -*- coding:utf-8 -*-
# copyright @Hchyeria
# 程序实践3

import math
from bitarray import bitarray


class HuffmanNode(object):
    """
    定义一个HuffmanNode虚类，里面包含两个虚方法：
    1. 获取节点的权重函数
    2. 获取此节点是否是叶节点的函数
    """

    def get_wieght(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'get_wieght'")

    def isleaf(self):
        raise NotImplementedError(
            "The Abstract Node Class doesn't define 'isleaf'")


class LeafNode(HuffmanNode):
    # 定义一个叶子节点类

    def __init__(self, value=0, freq=0):
        # 初始化叶子节点 需要初始化的参数 value及其出现的频率 freq
        super(LeafNode, self).__init__()
        # 节点的值
        self.value = value
        self.wieght = freq

    def isleaf(self):
        # 返回True，代表是叶节点
        return True

    def get_wieght(self):
        # 返回对象属性 weight，表示对象的权重
        return self.wieght

    def get_value(self):
        # 获取叶子节点的 字符 的值
        return self.value


class NomalNode(HuffmanNode):
    # 普通的节点类 也就是中间节点类

    def __init__(self, left_child=None, right_child=None):
        # 初始化普通的节点 需要初始化的对象参数 left_child, right_chiled
        super(NomalNode, self).__init__()

        # 节点的值
        self.wieght = left_child.get_wieght() + right_child.get_wieght()
        # 节点的左右子节点
        self.left_child = left_child
        self.right_child = right_child

    def isleaf(self):
        # 返回False，代表是中间节点
        return False

    def get_wieght(self):
        # 返回对象属性 weight，表示对象的权重
        return self.wieght

    def get_left(self):
        # 获取左子树
        return self.left_child

    def get_right(self):
        # 获取右子树
        return self.right_child


class HuffmanTree(object):

    def __init__(self, isNotLeafNode, value=0, wieght=0, left_tree=None, right_tree=None):

        super(HuffmanTree, self).__init__()

        if not isNotLeafNode:
            self.root = LeafNode(value, wieght)
        else:
            self.root = NomalNode(left_tree.get_root(), right_tree.get_root())

    def get_root(self):
        # 获取huffman tree 的根节点
        return self.root

    def get_wieght(self):
        # 获取这个huffman树的根节点的权重
        return self.root.get_wieght()

    def code_huffman_tree(self, root, huffman_code, char_freq):
        # 利用递归的方法遍历huffman_tree 得到每个 字符 对应的huffman编码保存在字典 char_freq中

        if not root.isleaf():
            self.code_huffman_tree(root.get_left(), huffman_code + '0', char_freq)
            self.code_huffman_tree(root.get_right(), huffman_code + '1', char_freq)
        else:
            char_freq[root.get_value()] = huffman_code
            print(
                ("key: %c  and  freq: %d  huffman_code: %s") % (chr(root.get_value()), root.get_wieght(), huffman_code))
            return None


def buildHuffmanTree(list_hufftrees):
    # 构造huffman树
    while len(list_hufftrees) > 1:
        # 根据weight大小 对huffman树进行从小到大的排序
        list_hufftrees.sort(key=lambda x: x.get_wieght())

        # 找出weight 最小的两个树
        temp1 = list_hufftrees[0]
        temp2 = list_hufftrees[1]
        list_hufftrees = list_hufftrees[2:]

        # 构造一个新的huffman树
        new_hufftree = HuffmanTree(1, 0, 0, temp1, temp2)

        list_hufftrees.append(new_hufftree)

    # 数组中最后剩下来的那棵树 就是构造的HuffmanTree
    return list_hufftrees[0]


class HuffmanCompressor:
    # 保存输出流
    output_buffer = None

    def canculateRate(self, input_file_path, debug=False):
        print("Canculateing Huffman......")
        # 获取文件名称 类型(扩展名)
        input_file_name, input_file_type = input_file_path.split('/')[-1].split('.')

        # 定义输出 bitarray 流
        output_buffer = bitarray(endian='big')
        # 读取文件
        try:
            with open(input_file_path, 'rb') as input_file:
                fileData = input_file.read()
        except IOError:
            print('Could not open input file ...')
            raise
        # 获取文件的总字节数
        pre_len = len(fileData)

        # 标识文件是用何种压缩算法 h 代表 Huffman l 代表 LZ77
        output_buffer.frombytes('h'.encode('utf-8'))

        # 储存文件的扩展名信息
        output_buffer.frombytes(input_file_type.encode('utf-8'))

        # 补充扩展名信息到 4 bytes
        while len(output_buffer) < 40:
            output_buffer.frombytes(b'0')

        # 统计 byte的每个值出现的频率 保存在字典 char_freq中
        char_freq = {}
        for x in range(pre_len):
            item = fileData[x]
            if item in char_freq.keys():
                char_freq[item] = char_freq[item] + 1
            else:
                char_freq[item] = 1

        # 输出统计结果
        if debug:
            for item in char_freq.keys():
                print(item, ' : ', char_freq[item])

        # 开始构造原始的huffman树数组 用于构造最终的Huffman树
        list_hufftrees = []
        for x in char_freq.keys():
            # 使用 HuffTree 的构造函数 定义一棵只包含一个叶节点的 Huffman树
            item = HuffmanTree(0, x, char_freq[x], None, None)
            # 将其添加到数组 list_hufftrees 当中
            list_hufftrees.append(item)


        # 储存叶节点的个数
        length = len(char_freq.keys())

        # 将其分成 4 bytes 写入到输出bitarray流当中
        output_buffer.frombytes(length.to_bytes(4, byteorder='big'))

        # 储存每个值 及其出现的频率的信息
        for x in char_freq.keys():
            # 储存每个值 分成 1 byte 写入
            output_buffer.frombytes(x.to_bytes(1, byteorder='big'))
            #
            temp = char_freq[x]
            # 出现的次数 分成 4 bytes 写入
            output_buffer.frombytes(temp .to_bytes(4, byteorder='big'))

        # 构造huffman编码树 并且获取到每个字符对应的 huffman 编码
        tem = buildHuffmanTree(list_hufftrees)
        tem.code_huffman_tree(tem.get_root(), '', char_freq)

        # 开始对文件进行压缩
        huffman_code = ''
        for i in range(pre_len):
            # 打印进度信息
            process = (i / pre_len) * 100
            print("process %d%% ..." % process)
            key = fileData[i]
            huffman_code = huffman_code + char_freq[key]

        out = 0
        while len(huffman_code) >= 8:
            for x in range(8):
                out = out << 1
                if huffman_code[x] == '1':
                    out = out | 1
            huffman_code = huffman_code[8:]
            output_buffer.frombytes(out.to_bytes(1, byteorder='big'))
            out = 0

        # 处理剩下来的不满8位的 huffman_code
        for i in range(len(huffman_code)):
            if huffman_code[i] == '1':
                output_buffer.append(True)
            else:
                output_buffer.append(False)

        # 用 0 填充 output_buffer 使它成为8的倍数
        output_buffer.fill()

        # 保留self.output_buffer属性 以便 compress() 函数使用
        self.output_buffer = output_buffer
        # 返回压缩率
        after_len = len(output_buffer)
        fraction = ((after_len / 8) / pre_len) * 100
        return fraction

    def compress(self, input_file_path, output_file_path=None, debug=False):
        print("Compressing ......")
        # 如果没有计算过并且保留self.output_buffer输出流 则执行canculateRate操作
        if not self.output_buffer:
            self.canculateRate(input_file_path)

        # 获取文件名称 类型(扩展名)
        input_file_name, input_file_type = input_file_path.split('/')[-1].split('.')

        # 写入文件 如果提供了 output_file_path 就在提供的 output_file_path 下写入 如果没有就同在 input_file_path 当前目录下写入文件
        if output_file_path:
            output_file_path_final = output_file_path + ("" if output_file_path[-1] == "/" else "/") + input_file_name + ".hchy"
        else:
            output_file_path_final = '/'.join(input_file_path.split('/')[0:-1]) + "/" + input_file_name + ".hchy"
        try:
            with open(output_file_path_final, 'wb') as output_file:
                output_file.write(self.output_buffer.tobytes())
                print("File was Huffman compressed successfully and saved to output path %s" % output_file_path_final)
                # 输出成功 关闭输出流
                output_file.close()
                return None
        except IOError:
            print('Eroor! Could not write to output file path %s' % output_file_path_final)
            raise

    def decompress(self, input_file_path, output_file_path, debug=False):
        print("Decompressing ......")
        # 获取文件名称 类型(扩展名)
        input_file_name, input_file_type = input_file_path.split('/')[-1].split('.')
        # 如果类型(扩展名)不是 hchy 则不是本软件压缩的文件无法解压缩
        if input_file_type == "hchy":
            # 定义读取文件的 bitarray 流
            data = bitarray(endian='big')
            # 定义输出流
            output_buffer = []
            # 读取文件
            try:
                with open(input_file_path, 'rb') as input_file:
                    data.fromfile(input_file)
            except IOError:
                print('Could not open input file ...')
                raise
            # 删除前面 1 byte 记录压缩算法类型的信息
            del data[0:8]
            # 取出前面 4 bytes 的扩展名信息 再删除
            type_byte = data[0:32].tobytes()
            del data[0:32]
            type_name = type_byte.decode('utf-8')
            # 除去不需要的为了填充为 4 bytes 的 0字符信息
            raw_index = type_name.find('0')
            if raw_index:
                type_name = type_name[0:raw_index]
            # 取出前面 4 bytes 的节点长度信息 再删除
            node_length = int.from_bytes(data[0:32].tobytes(), "big")
            del data[0:32]
            # 读取压缩文件中保存的原文件中每个值对应出现的频率的信息
            # 构造一个 字典 char_freq 重建 Huffman编码树
            char_freq = {}
            for i in range(node_length):
                # 取出 1 byte 的 key 信息 再删除
                key = int.from_bytes(data[0:8].tobytes(), "big")
                del data[0:8]
                # 取出 4 bytes 的 freq 信息 再删除
                value = int.from_bytes(data[0:32].tobytes(), "big")
                del data[0:32]

                if debug:
                    print(key, value)

                char_freq[key] = value

            # 重建 huffman 树
            list_hufftrees = []
            for x in char_freq.keys():
                item = HuffmanTree(0, x, char_freq[x], None, None)
                list_hufftrees.append(item)

            item = buildHuffmanTree(list_hufftrees)
            item.code_huffman_tree(item.get_root(), '', char_freq)

            # 用重建的huffman编码树 对压缩文件进行解压缩
            pre_len = len(data)
            # 获取重建的huffman编码树的根节点
            currnode = item.get_root()
            while len(data) > 0:
                # 打印解压进度消息
                process = ((pre_len - len(data)) / pre_len) * 100
                print("process %.2f%% ..." % process)
                # 如果是叶子节点则将 value 写入到输出
                if currnode.isleaf():
                    output_buffer.append(currnode.get_value().to_bytes(1, byteorder='big'))
                    currnode = item.get_root()
                # 如果为 b'1' 则向右移动
                if data[0] == True:
                    currnode = currnode.get_right()
                # 如果为 b'0' 则向左移动
                else:
                    currnode = currnode.get_left()
                # 删除前一位
                del data[0]
            # 处理剩余的
            if currnode.isleaf():
                output_buffer.append(currnode.get_value().to_bytes(1, byteorder='big'))
                currnode = item.get_root()
            # 连接 bytes list
            out_data = b''.join(output_buffer)
            # 输出文件 如果提供了 output_file_path 就在提供的 output_file_path 下写入 如果没有就同在 input_file_path 当前目录下写入文件
            if output_file_path:
                output_file_path_final = output_file_path + ("" if output_file_path[-1] == "/" else "/") + input_file_name+ "." + type_name
            else:
                output_file_path_final = '/'.join(input_file_path.split('/')[0:-1]) + "/" + input_file_name + "." + type_name
            try:
                with open(output_file_path_final, 'wb') as output_file:
                    output_file.write(out_data)
                    print('File was decompressed successfully and saved to output path %s' % output_file_path_final)
                    # 输出成功 关闭输出流
                    output_file.close()
                    return None
            except IOError:
                print('Could not write to output file path %s' % output_file_path_final)

                raise
        else:
            print("Error file type! It isn't .hchy. So can't be decompressed")

