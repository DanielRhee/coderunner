from flask import Flask, redirect, url_for,render_template, request
import codeRunner

app = Flask(__name__, template_folder="Site/", static_folder='/')

@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("page404"))

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
        global problemSet
        getLanguage = request.headers["language"]
        getProblem = request.headers["problemName"]
        #get the data and store it
        clientCode = request.get_data()

        try:
            for i in range(len(problemSet[getProblem][2])):
                runCode = codeRunner.runCode(getLanguage, request.get_data() , ''.join(list(map(str,problemSet[getProblem][2][i][0]))), getProblem)

                temp1 = str("".join(str(runCode).split())).replace("/n", "")
                temp2 = str("".join(str(problemSet[getProblem][2][i][1]).split())).replace("/n", "")
                print(len(temp1),len(temp2))
                temp3 = open("testing.txt",'w')
                temp3.write(temp1)
                temp3.write(temp2)

                if "".join(str(runCode).split()).replace("/n", "") != "".join(str(problemSet[getProblem][2][i][1]).split()).replace("/n", ""):
                    return render_template("output.html", codeOutput="Incorrect answer ❌ /n Testcase: /n" + str(problemSet[getProblem][2][i][0]).replace("\n","/n") + "/nExpected answer: /n" + str(problemSet[getProblem][2][i][1]) + "/nYour answer: /n" + str(runCode))
            return render_template("output.html", codeOutput="All Correct! ✅")
        except Exception as e:
            print(e)
            return render_template("output.html", codeOutput="An error occured, please try again later or if the issue persists the code broke lol. Also make sure you chose the right language.")
        
        #return render_template("output.html", codeOutput="An error occured, please try again later or if the issue persists the code broke lol. Also make sure you chose the right language.")
        
        #return render_template("editor.html", content="out"+count)

    return redirect(url_for("page404"))


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

        getFileName = request.headers["fileName"]

        try:
            return render_template("output.html", codeOutput=codeRunner.runCode(getLanguage, request.get_data(), "", getFileName))
        except:
            return render_template("output.html", codeOutput="An error occured, please try again later or if the issue persists the code broke lol. Also make sure you chose the right language.")
        
        #return render_template("editor.html", content="out"+count)

    return redirect(url_for("page404"))

@app.route("/404-Page-Not-Found")
def page404():
    return "<h1>Oops the page you're looking for does not exist</h1>"

"""@app.errorhandler(404)
def not_found(e):
    if request.path.endswith("/") and request.path[:-1] in all_endpoints:
        return redirect(request.path[:-1]), 302
    return redirect(url_for("page404"))"""

if __name__ == "__main__":
    #Problems
    global problemSet
    problemSet = {"TwoSum":["Given an array of numbers and a target, find two numbers in the array that add up to the target and return the sum of their indicies. You can assume there is exactly 1 solution. Use STDIN for input and use STDOUT for output","def twoSum(target,arr):", [["2 7 11 15 \n9",1],["3 2 4 \n6",3],["3 3 \n6",1]]]}
    #Format "Problem name":[Problem text, starting code, [[testcase1input, testcase1output], [testcase2input, testcase2output]]]
    
    app.run(port=5500, debug=True)
    app.url_map.strict_slashes = False