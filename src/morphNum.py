# Put documentation here
def morphNum(num1, num2, steps):
    
    output = []
    if num1 < num2:
        slope = (num2 - num1) / (steps - 0)
        print(slope)
        for x in range(steps):
            temp = int((slope * x) + num1)
            output.append(temp)
        return output

    elif num1 > num2:
        slope = (num1 - num2) / (steps - 0)
        for x in range(steps):
            temp = int((slope * x) + num2)
            output.append(temp)
        return output

    elif num1 == num2:
        for x in range(steps):
            output.append(num1)
        return output