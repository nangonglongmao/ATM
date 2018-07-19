'''
验证码：
string_len：验证码长度
string_type:验证码类型：0:纯数字；1：纯字母；2：字母数字混合
'''
import random
while True:
    def s(string_len,string_type):
        yzm=''
        if string_type==0:
            for i in range(string_len):
                yzm+=str(random.randint(0,9))#yzm+=str(random.randint(0,9))
        if string_type==1:
            for j in range(string_len):
                n=random.randint(0,1)
                if n==0:
                    yzm+=chr(random.randint(97,122))
                else:
                    yzm+=chr(random.randint(65,90))
        if string_type==2:
            for k in range(string_len):
                n = random.randint(0, 2)
                if n == 0:
                    yzm += chr(random.randint(97, 122))
                elif n==1:
                    yzm += chr(random.randint(65, 90))
                else:
                    yzm += str(random.randint(0, 9))

        return yzm
    n1=int(input('请输入字符串长度：'))
    n2=int(input('请输入字符串类型：'))
    print(s(n1,n2))