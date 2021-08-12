x = input()
print(x + "bleb")

arr = list(map(int,input().split()))
target = int(input())

seen = {}
for i in range(len(arr)):
    if target-arr[i] in seen:
        print(i + seen[target-arr[i]])
        break
    seen[arr[i]] = i