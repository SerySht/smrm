
def QuickSort(A, l, r):
    if l >= r:
        return
    else:
        m = A[(l + r) / 2]
        i = l
        j = r
        while i <= j:
            while A[i] < m:
                i += 1

            while A[j] > m:
                j -= 1
            if i <= j:
                A[i], A[j] = A[j], A[i]
                i += 1
                j -= 1
                QuickSort(A, l, j)
                QuickSort(A, i, r)




def megre(l, r):
    new_list = []

    while l and r:
        if l[0] < r[0]:
            new_list.append(l.pop(0))
        else:
            new_list.append(r.pop(0))
    if l:
        new_list.extend(l)
    if r:
        new_list.extend(r)
    return  new_list

def MergeSort(A):
    if len(A) >= 2:
        mid = int(len(A) / 2)
        A = megre(MergeSort(A[:mid]), MergeSort(A[mid:]))
    return  A



def radixsort(A):
    length = len(str(max(A)))
    rang = 10
    for i in range(length):
      B = [[] for k in range(rang)]
      for x in A:
          n = x // 10**i % 10
          B[n].append(x)
      A = []
      for k in range(rang):
         A = A + B[k]
    return A

if __name__ == "__main__":
    pass
