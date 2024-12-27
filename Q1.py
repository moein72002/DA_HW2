import sys
import heapq

n, d = list(map(int, input().split()))
a = list(map(int, input().split()))

a = [0]+a
visited = [False]*(n+1)

plusHeap = []
minusHeap = []

for i in range(1,n+1):
    heapq.heappush(plusHeap, (a[i]-d*i, i))
    heapq.heappush(minusHeap,(a[i]+d*i, i))

visited[1]=True
MST_cost=0
count_visited=1

minAplus = a[1]+d*1
minAminus= a[1]-d*1

while count_visited<n:
    # clean visited
    while plusHeap and visited[plusHeap[0][1]]:
        heapq.heappop(plusHeap)
    while minusHeap and visited[minusHeap[0][1]]:
        heapq.heappop(minusHeap)

    plus_key, pnode = plusHeap[0]
    minus_key,mnode= minusHeap[0]

    candidate_from_plus = plus_key + minAplus
    candidate_from_minus= minus_key + minAminus

    if candidate_from_plus < candidate_from_minus:
        chosen_dist = candidate_from_plus
        chosen_node = pnode
    else:
        chosen_dist = candidate_from_minus
        chosen_node = mnode

    visited[chosen_node]=True
    MST_cost+=chosen_dist
    count_visited+=1

    if a[chosen_node]+d*chosen_node<minAplus:
        minAplus=a[chosen_node]+d*chosen_node
    if a[chosen_node]-d*chosen_node<minAminus:
        minAminus=a[chosen_node]-d*chosen_node

print(MST_cost)
