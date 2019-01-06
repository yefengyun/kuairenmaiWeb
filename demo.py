from hashlib import md5

if __name__ == '__main__':
    md = md5()
    md.update("123456".encode('utf-8'))
    # 获取sign
    sign = md.hexdigest()
    print(sign)
