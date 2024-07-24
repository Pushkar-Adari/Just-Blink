coins = [1000,100,50,20,10,5,2,1]
total = int(input())
change = []
for coin in coins:
  if coin <= total:
    n = int(total/coin)
    total = total - coin * n
    for i in range(n):
      change.append(coin)
if len(change) == 0:
  print("0")
for c in change:
  print(c,end = '  ')