import pyupbit

access = "3vC7Q12XjxlmzckKZ7elpnDX4laOGvdpWDg1c1SX"          # 본인 값으로 변경
secret = "ZHxx7UViBtl6xJ74LzF7C1oH0cQtELw4tBNzGuNJ"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-ETC"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
