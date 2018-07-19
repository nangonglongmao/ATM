

'''
银行自动提款机系统：
    分析：
        人:
            类名：Person
            属性：姓名、身份证号、电话号、卡
            行为：
        
        卡:
            类名：Card
            属性：卡号、密码、余额
            行为：
            
        
        提款机：
            类名：ATM
            属性：用户字典
            行为：开户、取款、存款、转账、改密吧、锁定、解锁、补卡、销户
            
        管理员：
            类名：Admin
            属性：
            行为：管理员界面、管理员验证、系统功能界面
'''
#界面：
import time
import pickle
import os

class Admin(object):
    admin ='1'
    password='1'

    def printAdminView(self):
        print('***********************************************')
        print('*                                             *')
        print('*                                             *')
        print('*           欢迎登录赵氏国际银行                *')
        print('*                                             *')
        print('*                                             *')
        print('***********************************************')




    def printSysFunctionView(self):
        print('********************************************** ')
        print('*                                             *')
        print('*      开户（1)               查询（2）        *')
        print('*      取款（3)               存款（4）        *')
        print('*      转账（5)               改密（6）        *')
        print('*      锁定（7)               解锁（8）        *')
        print('*      补卡（9)               销户（0）        *')
        print('*               退出（quit）                   *')
        print('*                                             *')
        print('********************************************** ')

    def adminOption(self):
        inputadmin = input('请输入管理员账号：')
        if self.admin != inputadmin:
            print('账号输入有误！！！')
            return -1
        inputpassword = input('请输入管理密码：')
        if self.password != inputpassword:
            print('密码输入有误！！！')
            return -1
        # 能执行到这里说明账号密码正确！
        print('操作成功！请稍后...')
        time.sleep(2)
        return 0

class User:
    def __init__(self,name ,idCard,phone,card):
        self.name=name
        self.idCard=idCard
        self.phone=phone
        self.card=card


class Card:
    def __init__(self,cardId,cardPassword,cardMoney):
        self.cardId=cardId
        self.cardPassword=cardPassword
        self.cardMoney=cardMoney
        self.cardLock=False


import random
class ATM:
    def __init__(self,allUsers):
        self.allUsers=allUsers#卡号<==>用户


    #开户
    def createUser(self):
        #目标：向用户字典中添加一段键值对（卡号：用户）
        name=str(input('请输入您的姓名：'))
        idCard=int(input('请输入您的身份证号：'))
        phone=input('请输入您的电话号码：')
        prestoreMoney=int(input('请输入预存款金额：'))
        if prestoreMoney<0:
            print('预存款输入有误！！！开户失败...')
            return -1

        onePasswd=input('请设置密码：')
        #验证密码：
        if not self.checkPasswd(onePasswd):
            print('密码输入错误！！！开户失败...')
            return 1

        #所有需要的信息就全了
        cardStr=self.randomCardId()
        card=Card(cardStr,onePasswd,prestoreMoney)

        user=User(name,idCard,phone,card)
        #存到字典
        self.allUsers[cardStr]=user
        print('开户成功！请牢记卡号:{}！'.format(cardStr))


    #查询
    def searchUserInfo(self):
        cardNum=input('请输入您的卡号：')
        #验证是否存在该卡号
        user=self.allUsers.get(cardNum)
        if not user:
            print('该卡号不存在！！！查询失败...')
            return -1
        #判断是否锁定：
        if user.card.cardLock:
            print('该卡已被锁定！！！请解锁后再进行造作...')
            return -1
         #验证密码：
        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！该卡已被锁定！！！请解锁后再进行造作...')
            user.card.cardLock=True
            return -1
        print('账号：{} 余额：{}'.format(user.card.cardId,user.card.cardMoney))


    #取款
    def getMoney(self):
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号：
        user = self.allUsers.get(cardNum)
        if not user:
            print('该卡号不存在！！！取款失败...')
            return -1
        # 判断是否锁定：
        if user.card.cardLock:
            print('该卡已被锁定！！！请解锁后再进行造作...')
            return -1
        # 验证密码：
        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！该卡已被锁定！！！请解锁后再进行造作...')
            user.card.cardLock = True
            return -1
        #金额判断：
        money=int(input('请输入取款金额：'))
        if money>user.card.cardMoney:
            print('金额不足！！！取款失败...')
            return -1
        if money <=0:
            print('输入错误！！！取款失败...')
            return -1
        #取款：
        user.card.cardMoney-=money
        print('取款成功！！！余额：{}'.format(user.card.cardMoney))


    #存款
    def saveMoney(self):
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号：
        user = self.allUsers.get(cardNum)
        if not user:
            print('该卡号不存在！！！取款失败...')
            return -1
        # 判断是否锁定：
        if user.card.cardLock:
            print('该卡已被锁定！！！请解锁后再进行造作...')
            return -1
        # 验证密码：
        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！该卡已被锁定！！！请解锁后再进行造作...')
            user.card.cardLock = True
            return -1
        # 金额判断：
        money = int(input('请输入存款金额：'))
        if money <=0:
            print('输入错误！！！取款失败...')
            return -1
        # 存款：
        user.card.cardMoney += money
        print('存款成功！！！余额：{}'.format(user.card.cardMoney))


    #转账
    def transferMoney(self):
        # 转账对象：
        otherCardNum = input('请输入对方的卡号：')
        user1 = self.allUsers.get(otherCardNum)
        if not otherCardNum:
            print('该卡号不存在！！！转账失败...')
            return -1
        # 判断对方账户是否锁定：
        if user1.card.cardLock:
            print('对方账户已锁定！！！无法转账...')
            return -1
        print('转账接收者信息：')
        print('对方卡号：{}，姓名：{}，'.format(otherCardNum,user1.name))
        determine=str(input('是否转账（Y/N）：'))
        if determine=='N':
            print('转账已取消...')
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号：
        user = self.allUsers.get(cardNum)
        if not user:
            print('您的号不存在！！！转账失败...')
            return -1
        # 判断是否锁定：
        if user.card.cardLock:
            print('您的卡已被锁定！！！请解锁后再进行造作...')
            return -1
        # 验证密码：
        if not self.checkPasswd(user.card.cardPassword):
            print('您的密码输入错误！！！该卡已被锁定！！！请解锁后再进行造作...')
            user.card.cardLock = True
            return -1
        #金额判断：
        money1 = int(input('请输入存款金额：'))
        if money1 <= 0:
            print('输入错误！！！取款失败...')
            return -1
        # 转账：
        user1.card.cardMoney += money1
        user.card.cardMoney -= money1
        print('转账成功！！！您的余额：{}'.format(user.card.cardMoney))


    #改密
    def changePasswd(self):
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号：
        user = self.allUsers.get(cardNum)
        if not user:
            print('该卡号不存在！！！取款失败...')
            return -1
        # 判断是否锁定：
        if user.card.cardLock:
            print('该卡已被锁定！！！请解锁后再进行造作...')
            return -1
        # 验证密码：
        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！该卡已被锁定！！！请解锁后再进行造作...')
            user.card.cardLock = True
            return -1
        while True:
            newPassword=input('请输入新密码：')
            twoPassword=input('请再次输入新密码：')
            if newPassword==twoPassword:
                user.card.cardPassword=newPassword
                break;
        else:
            print('两次输入的密码不相同,请重新输入：')


    #锁定
    def lockUser(self):
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号
        user = self.allUsers.get(cardNum)
        if not user:
            print('该卡号不存在！！！锁定失败...')
            return -1

        if user.card.cardLock:
            print('该卡已经被锁定！！！请解锁后再使用其他功能...')
            return -1

        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！锁定失败...')
            return -1

        tempIdCard = input('请输入您的身份证号：')
        if tempIdCard != user.idCard:
            print('身份证号输入错误！！！锁定失败...')
        # 锁卡：
        user.card.cardLock = True
        print('锁定成功...')


    #解锁
    def unlockUser(self):
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号
        user = self.allUsers.get(cardNum)
        if not self.allUsers.get(cardNum):
            print('该卡号不存在！！！解锁失败...')
            return -1

        if not user.card.cardLock:
            print('该卡没有被锁定！无需解锁...')
            return -1

        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！解锁失败...')
            return -1

        tempIdCard = input('请输入您的身份证号：')
        if tempIdCard != user.idCard:
            print('身份证号输入错误！！！解锁失败...')
            return -1
        #解锁：
        user.card.cardLock=False
        print('解锁成功...')


    #补卡
    def newCard(self):
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号：
        user = self.allUsers.get(cardNum)
        if not user:
            print('该卡号不存在！！！补卡失败...')
            return -1
        # 判断是否锁定：
        if user.card.cardLock:
            print('该卡已被锁定！！！请解锁后再进行造作...')
            return -1
        # 验证密码：
        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！该卡已被锁定！！！请解锁后再进行造作...')
            user.card.cardLock = True
            return -1
        newCardStr = self.randomCardId()
        # 存到字典
        self.allUsers[newCardStr] = user
        print('补卡成功！请牢记卡号:{}！'.format(newCardStr))


    #销户
    def killUser(self):
        cardNum = input('请输入您的卡号：')
        # 验证是否存在该卡号：
        user = self.allUsers.get(cardNum)
        if not user:
            print('该卡号不存在！！！补卡失败...')
            return -1
        # 判断是否锁定：
        if user.card.cardLock:
            print('该卡已被锁定！！！请解锁后再进行造作...')
            return -1
        # 验证密码：
        if not self.checkPasswd(user.card.cardPassword):
            print('密码输入错误！！！该卡已被锁定！！！请解锁后再进行造作...')
            user.card.cardLock = True
            return -1
        del  self.allUsers[cardNum]
        print('销户成功...')

    # 验证密码：
    def checkPasswd(self,realPasswd):
        for i in range (3):
            tempPasswd=input('请输入密码：')
            if tempPasswd==realPasswd:
                return True
        return False

    #生成卡号：
    def randomCardId(self):
        while True:
            str = ''
            for i in range(6):
                ch = chr(random.randrange(ord('0'), ord('9') + 1))
                str += ch
                #判断是否重复
            if not self.allUsers.get(str):
                return str


def main():
    #管理员对象
    admin = Admin()
    # 管理员开机
    admin.printAdminView()
    if admin.adminOption():
            return -1

    #存储所有用户的信息：
    allUsers={}

    #提款机对象
    filepath = os.path.join(os.getcwd(), 'allusers.txt')
    f=open(filepath,'rb')
    allUsers=pickle.load(f)
    print(allUsers)

    #allUsers={}#先用空字典写入
    atm=ATM(allUsers)



    while True:
        admin.printSysFunctionView()
        #等待用户的操作：
        option=str(input('请输入您的操作：'))
        if option=='1':
            #开户：
            atm.createUser()
        elif option=='2':
            #查询：
            atm.searchUserInfo()
        elif option == '3':
            #取款：
            atm.getMoney()
        elif option == '4':
            #存款：
            atm.saveMoney()
        elif option == '5':
            #转账：
            atm.transferMoney()
        elif option == '6':
            #改密：
            atm.changePasswd()
        elif option == '7':
            #锁定：
            atm.lockUser()
        elif option == '8':
            #解锁：
            atm.unlockUser()
        elif option == '9':
            #补卡：
            atm.newCard()
        elif option=='0':
            #销户：
            atm.killUser()
        elif option=='quit':
            #退出：
           if not admin.adminOption():
            #将当前系统中的用户信息保存到文件中
            filepath=os.path.join(os.getcwd(),'allusers.txt')
            f=open(filepath,'wb')
            pickle.dump(atm.allUsers,f)
            f.close()
            return -1

    time.sleep(2)


if __name__=='__main__':
    main()


















