import numpy as np

width = 6830
height = 2000

max_for_png = 100
multiplier_ratio = 32
start_index = 13660

def convert_img_to_numpy_array(file):
    with open(file, "rb") as f:
        raw_data = f.read()
    if raw_data[:7] != b"ipdsc\x00;":
        raise Exception("Could not interpret magic string")
    dtype = np.dtype(np.uint16)
    # start_index以降に2byteずつintensityの値が格納されている。
    data = np.frombuffer(raw_data[start_index:], dtype).copy().reshape(height, width)
    data = data.astype(dtype)
    data = data.byteswap(True)
    data = data[::-1]
    dtype = np.dtype(np.uint32)
    data = data.astype(dtype)

    # intensityが2**15以上のときはその値から2**15を引いて、定数multiplier_ratioを掛ける。
    # 手持ちのデータはすべて32でOKだが、要確認。
    data = np.where(data >= 2**15, (data - 2**15) * multiplier_ratio, data) 
    return data