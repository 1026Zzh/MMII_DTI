import numpy as np
import json

def get_all_smiles():
    max_len = 0
    smiles = []
    # types = {"human"}
    types = {"Davis"}
    # types = {"celegans"}
    # types = {"KIBA"}
    for type in types:
        data_file = "common/case_study_target_Davis_test/" + type + "_smile_features.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()
            for i in lines:
                smiles.append(i.split("\n")[0])
                max_len = max(max_len, len(i))
    print("max_len: ", max_len)
    return smiles


def seq_to_kmers(seq, k):
    N = len(seq)
    return [seq[i:i + k] for i in range(N - k + 1)]


def get_k_gram_seqs(smiles, k):
    smile_seq = []
    for smile in smiles:
        smi = ""
        for i in smile:
            smi += i

        smile_seq.append(seq_to_kmers(smi, k=k))
    return smile_seq


def get_k_gram_seq(smile, k):
    smi = ""
    for i in smile:
        smi += i
    smi = seq_to_kmers(smi, k=k)
    return smi


def get_dict(smiles):
    num = float(1.0)
    dict = {}
    for seq in smiles:
        line = []
        for i in seq:
            if i not in dict:
                dict[i] = num
                num += float(1.0)
            line.append(dict[i])
    return dict


def k_gram_save(data_file, k, save_name):
    with open(data_file, 'r') as f:
        data_list = f.read().strip().split('\n')

    N = len(data_list)
    print("drug----数据集大小", N)
    smiles = []
    all = 0
    num = 0
    max_len = 0
    num_max = 0
    for i, data in enumerate(data_list):
        lis = []
        smile = data.strip()

        all += len(smile)
        num += 1

        smi = get_k_gram_seq(smile, k)
        for seq in smi:
            lis.append(float(dict[seq]))
        max_len = max(max_len, len(lis))
        if len(lis) > dim:
            lis = lis[0:dim]
        while len(lis) < dim:
            lis.append(0.)
        num_max = max(max(lis), num_max)

        smiles.append(lis)
    print("平均长度:", all / num)
    print("最大长度:", max_len)
    print("分成不同种类数:", num_max)

    # 将列表的列表转换为二维NumPy数组
    smiles_array = np.array(smiles)

    print(smiles_array.shape)

    # 保存为json文件
    with open(save_name + ".txt", 'w') as f:
        # 转换浮点数为整数
        json.dump(smiles_array.astype(int).tolist(), f)
        f.close()


if __name__ == '__main__':
    k = 1
    dim = 512
    smiles = get_k_gram_seqs(get_all_smiles(), k)
    dict = get_dict(smiles)
    print(dict)

    # types = {"human"}
    types = {"Davis"}
    # types = {"celegans"}
    # types = {"KIBA"}
    for type in types:
        data_file = "common/case_study_target_Davis_test/" + type + "_smile_features.txt" #药物化学文本信息
        save_name = "common/case_study_target_Davis_test/" + type + "_smiles_" + str(k) + "_gram"
        print(data_file)

        k_gram_save(data_file=data_file, k=k, save_name=save_name)
