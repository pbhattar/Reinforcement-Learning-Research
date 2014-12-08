'''Finds number of combs for BlocksWorld'''

def subset_sum_recursive(numbers,target,partial, combinations):
    s = sum(partial)
    partial = sorted(partial)
    #check if the partial sum is equals to target
    if s == target and partial not in combinations:
    #print "sum(%s)=%s"%(partial,target)
        #print partial
        combinations.append(partial)
    if s >= target:
        return # if we reach the number why bother to continue
    
    for i in range(len(numbers)):
        n = numbers[i]
        #remaining = numbers[i+1:]
        subset_sum_recursive(numbers,target,partial + [n], combinations)

def subset_sum(numbers,target, combinations):
    #we need an intermediate function to start the recursion.
    #the recursion start with an empty list as partial solution.
    subset_sum_recursive(numbers,target,list(), combinations)

def findCombs(num):
    combinations = []
    subset_sum(range(1,num+1),num, combinations)
    return combinations
    


    
        
        
    
