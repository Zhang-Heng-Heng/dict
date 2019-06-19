import getpass
import hashlib

#输入隐藏
pwd=getpass.getpass("pw:")
print(pwd)

#做转换加密
# hash=hashlib.md5()#生成对象
# hash.update(pwd.encode())#算法加密
#算法加盐
hash=hashlib.md5("@#!%$&*".encode())#生成对象
hash.update(pwd.encode())#算法加密
pwd=hash.hexdigest()#提取加密后的密码
print(pwd)