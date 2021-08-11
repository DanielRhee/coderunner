def runCode(lang, code, codeInput):
    import random
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    randomString = ""
    for i in range(50):
        randomString += alphabet[random.randint(0,len(alphabet)-1)]

    if lang == "python":
        f = open(randomString+".py","w")
        #turn binary into normal stuff and write it
        f.write(bytes.decode(code))
        f.close()

        #print(str(problemSet[getProblem][2][0]))
        result = subprocess.Popen(["python3", randomString +".py"], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #print(''.join(list(map(str,problemSet[getProblem][2][0][0]))).encode())
        result.stdin.write(codeInput.encode())
        #result.stdin.write(''.join(list(map(str,problemSet[getProblem][2][0][0]))).encode())
        out, err = result.communicate()

        #process = subprocess.Popen("python3 " + randomString +".py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #out, err = process.communicate()
        #errcode = process.returncode   
        os.remove(randomString+".py")   

    elif lang == "cpp":
        f = open(randomString+".cpp","w")
        #turn binary into normal stuff and write it
        f.write(bytes.decode(code))
        f.close()

        process = subprocess.Popen("g++ -o ./" + randomString +" ./" + randomString + ".cpp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        #print(err)

        result = subprocess.Popen(["./" + randomString], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result.stdin.write(codeInput.encode())
        out, err = result.communicate()

        """
        process = subprocess.Popen("./" + randomString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        errcode = process.returncode   
        """
        os.remove(randomString+".cpp") 
        try:
            os.remove(randomString)
        except: 
            1+1

    elif lang == "c":
        f = open(randomString+".c","w")
        #turn binary into normal stuff and write it
        f.write(bytes.decode(code))
        f.close()

        process = subprocess.Popen("g++ -o ./" + randomString +" ./" + randomString + ".c", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        #print(err)
        result = subprocess.Popen(["./" + randomString], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result.stdin.write(codeInput.encode())
        out, err = result.communicate()
        """process = subprocess.Popen("./" + randomString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()"""
        errcode = process.returncode   
        os.remove(randomString+".c") 
        try:
            os.remove(randomString)
        except: 
            1+1

    elif lang == "java":
        f = open(randomString+".java","w")
        #turn binary into normal stuff and write it
        writeToFileTemp = bytes.decode(code)
        #print(writeToFileTemp.count("class Main"))
        writeToFileTemp = writeToFileTemp.replace("class Main", "class "+randomString)
        writeToFileTemp = writeToFileTemp.replace("class main", "class "+randomString)
        f.write(writeToFileTemp)
        #f.write("public class " + randomString)
        f.close()
        
        process = subprocess.Popen("javac " + randomString +".java", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        result = subprocess.Popen(["java", randomString], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result.stdin.write(codeInput.encode())
        out, err = result.communicate()

        """
        process = subprocess.Popen("java " + randomString , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()"""
        errcode = process.returncode   
            
        os.remove(randomString+".java") 
        try:    
            os.remove(randomString+".class")
        except:
            1+1
    if bytes.decode(out) != "":
        return bytes.decode(out)
    return bytes.decode(err)