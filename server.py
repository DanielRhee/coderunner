from flask import Flask, redirect, url_for,render_template, request
import codeRunner

app = Flask(__name__, template_folder="Site/", static_folder='/')

#Pages
@app.route("/problems")
def problems():
    return render_template("Problems/problemHome.html")

@app.route("/problems/<problemName>")
def problem(problemName):
    global problemSet
    if problemName in problemSet:
        return render_template("Problems/problemDisplay/problemDisplay.html", problemName = problemName, problemText = problemSet[problemName][0], startingCodeTemplate = problemSet[problemName][1])
    return redirect(url_for("page404"))

@app.route("/submitProblemForJudging", methods=["POST","GET"])
def submitProblemForJudging():
    if request.method == "POST":
        getLanguage = request.headers["language"]
        getProblem = request.headers["problemName"]
       
        import random
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        randomString = ""
        for i in range(50):
            randomString += alphabet[random.randint(0,len(alphabet)-1)]
        #get the data and store it
        clientCode = request.get_data()

        

    return render_template("output.html", codeOutput="lol")
    #return render_template("output.html", codeOutput=out.replace(randomString,"filename"))


@app.route("/runProblemNoJudging", methods = ["POST", "GET"])
def runProblemNoJudging():
    if request.method == "POST":
        global problemSet
        getLanguage = request.headers["language"]
        getProblem = request.headers["problemName"]
        import random
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        randomString = ""
        for i in range(50):
            randomString += alphabet[random.randint(0,len(alphabet)-1)]
        #get the data and store it
        clientCode = request.get_data()

        if getLanguage == "python":
            f = open(randomString+".py","w")
            #turn binary into normal stuff and write it
            f.write(bytes.decode(clientCode))
            f.close()

            #print(str(problemSet[getProblem][2][0]))
            result = subprocess.Popen(["python3", randomString +".py"], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            #print(''.join(list(map(str,problemSet[getProblem][2][0][0]))).encode())
            result.stdin.write(''.join(list(map(str,problemSet["TwoSum"][2][0][0]))).encode())
            #result.stdin.write(''.join(list(map(str,problemSet[getProblem][2][0][0]))).encode())
            out, err = result.communicate()

            #process = subprocess.Popen("python3 " + randomString +".py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #out, err = process.communicate()
            #errcode = process.returncode   
            os.remove(randomString+".py")   

        elif getLanguage == "cpp":
            f = open(randomString+".cpp","w")
            #turn binary into normal stuff and write it
            f.write(bytes.decode(clientCode))
            f.close()

            process = subprocess.Popen("g++ -o ./" + randomString +" ./" + randomString + ".cpp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            #print(err)

            result = subprocess.Popen(["./" + randomString], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result.stdin.write(' '.join(list(map(str,problemSet[getProblem][2][0][0]))).encode())
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

        elif getLanguage == "c":
            f = open(randomString+".c","w")
            #turn binary into normal stuff and write it
            f.write(bytes.decode(clientCode))
            f.close()

            process = subprocess.Popen("g++ -o ./" + randomString +" ./" + randomString + ".c", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            #print(err)
            result = subprocess.Popen(["./" + randomString], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result.stdin.write(' '.join(list(map(str,problemSet[getProblem][2][0][0]))).encode())
            out, err = result.communicate()
            """process = subprocess.Popen("./" + randomString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()"""
            errcode = process.returncode   
            os.remove(randomString+".c") 
            try:
                os.remove(randomString)
            except: 
                1+1

        elif getLanguage == "java":
            f = open(randomString+".java","w")
            #turn binary into normal stuff and write it
            writeToFileTemp = bytes.decode(clientCode)
            #print(writeToFileTemp.count("class Main"))
            writeToFileTemp = writeToFileTemp.replace("class Main", "class "+randomString)
            writeToFileTemp = writeToFileTemp.replace("class main", "class "+randomString)
            f.write(writeToFileTemp)
            #f.write("public class " + randomString)
            f.close()
        
            process = subprocess.Popen("javac " + randomString +".java", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

            result = subprocess.Popen(["java", randomString], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            result.stdin.write(str(' '.join(list(map(str,problemSet[getProblem][2][0][0])))).encode())
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


        out = bytes.decode(out)
        if out != "":
            f = open(randomString+".txt",'w')
            f.write(out)
            f.write("Expected output: ")
            f.write(str(problemSet[getProblem][2][0][1]))
            f.close()
            f = open(randomString+".txt",'r')
            arr = f.readlines()
            f.close()
            os.remove(randomString+".txt")
            out = "/n ".join(arr)
            #print(out.count("/n"))
            #print(out)
            return render_template("output.html", codeOutput=out)
        #print(err)
        return render_template("output.html", codeOutput=err)

@app.route("/sandbox", methods=["POST","GET"])
def sandbox():
    return render_template("sandbox/editor.html")

@app.route("/runSandbox", methods=["POST","GET"])
def runSandbox():
    
    if request.method == "POST":

        #get language extension
        getLanguage = request.headers["language"]

        #try:
        return render_template("output.html", codeOutput=codeRunner.runCode(getLanguage, request.get_data(), ""))
        #except:
        #    return render_template("output.html", codeOutput="An error occured, please try again later or if the issue persists the code broke lol. Also make sure you chose the right language.")
        
        #return render_template("editor.html", content="out"+count)

    return redirect(url_for("page404"))

@app.route("/404-Page-Not-Found")
def page404():
    return "<h1>Oops the page you're looking for does not exist</h1>"

if __name__ == "__main__":
    #Problems
    global problemSet
    problemSet = {"TwoSum":["Given an array of numbers and a target, find two numbers in the array that add up to the target and return their indicies. You can assume there is exactly 1 solution. Use STDIN for input and use STDOUT for output","def twoSum(target,arr):", [["2 3 4 5 6 7 8 \n5",5]]]}
    #Format "Problem name":[Problem text, starting code, [[testcase1input, testcase1output], [testcase2input, testcase2output]]]
    
    app.run(port=5500, debug=True)