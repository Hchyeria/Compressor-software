from LZ77 import LZ77Compressor
from Huffman import HuffmanCompressor


LZ77Compressor = LZ77Compressor(window_size=20) # 可自定义 window_size 默认为 20
HuffmanCompressor = HuffmanCompressor()


type = input('Compress or Decompress? type c/d:')
if type == 'c':
    input_file_path = input('Input file path: ')
    output_file_path = input('Output file path: ')
    LZ77Rate = LZ77Compressor.canculateRate(input_file_path, debug=True)
    HuffmanRate = HuffmanCompressor.canculateRate(input_file_path, debug=True)
    print("LZ77 CompressRate: %.2f%%, Huffman CompressRate: %.2f%%" % (LZ77Rate, HuffmanRate))
    if LZ77Rate <= HuffmanRate:
        print("We choose the better LZ77Compressor to compress")
        contine = input('Are you contine LZ77Compressor? y/n')
        if contine == 'y':
            LZ77Compressor.compress(input_file_path, output_file_path)
        else:
            contine_other = input('Do you want to choose another HuffmanCompressor? y/n')
            if contine_other == 'y':
                HuffmanCompressor.compress(input_file_path, output_file_path)
            else:
                print("Thank your use!")
    else:
        print("We choose the better HuffmanCompressor to compress...")
        contine = input('Are you contine HuffmanCompressor? y/n')
        if contine == 'y':
            HuffmanCompressor.compress(input_file_path, output_file_path)

        else:
            contine_other = input('Do you want to choose another LZ77Compressor? y/n')
            if contine_other == 'y':
                LZ77Compressor.compress(input_file_path, output_file_path)
            else:
                print("Thank your use!")

elif type == 'd':
    input_file_path = input('Input file path: ')
    output_file_path = input('Output file path: ')
    try:
        with open(input_file_path, 'rb') as input_file:
            data = input_file.read(1)
    except IOError:
        print('Could not open input file ...')
        raise
    type_char = data.decode('utf-8')
    if type_char == 'h':
        HuffmanCompressor.decompress(input_file_path, output_file_path)
    elif type_char == 'l':
        LZ77Compressor.decompress(input_file_path, output_file_path)
    else:
        # 如果没有相应的算法类型信息 则不是本软件压缩的文件无法解压缩
        print("Error file type! It isn't .hchy. So can't be decompressed")

else:
    print("Please type 'c' represent Compress and type 'd' represent Decompress")


