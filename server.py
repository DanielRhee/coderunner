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
        #get the data and store it
        clientCode = request.get_data()

        try:
            return render_template("output.html", codeOutput= "Your Output: /n" + codeRunner.runCode(getLanguage, request.get_data() , ''.join(list(map(str,problemSet[getProblem][2][0][0]))), getProblem) + "Expected Output: /n" + str(problemSet[getProblem][2][0][1]))
        except:
            return render_template("output.html", codeOutput="An error occured, please try again later or if the issue persists the code broke lol. Also make sure you chose the right language.")
        
        #return render_template("editor.html", content="out"+count)

    return redirect(url_for("page404"))

@app.route("/sandbox", methods=["POST","GET"])
def sandbox():
    return render_template("sandbox/editor.html")

@app.route("/runSandbox", methods=["POST","GET"])
def runSandbox():
    
    if request.method == "POST":

        #get language extension
        getLanguage = request.headers["language"]

        try:
            return render_template("output.html", codeOutput=codeRunner.runCode(getLanguage, request.get_data(), "", "Sandbox"))
        except:
            return render_template("output.html", codeOutput="An error occured, please try again later or if the issue persists the code broke lol. Also make sure you chose the right language.")
        
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