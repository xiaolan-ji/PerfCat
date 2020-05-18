class Solution:
    def __init__(self):
        self.res = 0
        self.val = []
    def sumNums(self, n: int) -> int:
        # print(n)
        # if n == 1:
        #     return 1
        # print(n)
        # print("###")
        #
        # t = self.sumNums(n - 1)
        # print("++++")
        # print(t)
        # print("n=%d" %(n))
        # n += t
        # print(n)
        # print("___")
        # return n
        if n == 1:
            return 1
        self.res += self.sumNums(n-1)
        print(self.res)
        return self.res

if __name__ == "__main__":
    s = "cn.jj"
    s2 = "cn.jj.service"
    s3 = "cn.jj"
    print(id(s))
    print(id(s3))
