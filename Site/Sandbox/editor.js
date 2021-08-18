var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");
editor.setShowPrintMargin(false);

var currentLanguage = "python"

function startEnvironment() {
    changeLanguage();
    document.getElementById("fileName").value = "Main.py"
    //console.log()
}

function executeCode() {
    const format = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
    let validFileExtensions = ["java", "py", "cpp", "c"]

    //console.log(!format.test(document.getElementById("fileName").value.split(".")[0]));
    //console.log((document.getElementById("fileName").value.split(".")[1] == undefined || validFileExtensions.includes(document.getElementById("fileName").value.split(".")[1])));

    if (!format.test(document.getElementById("fileName").value.split(".")[0]) && (document.getElementById("fileName").value.split(".")[1] == undefined || validFileExtensions.includes(document.getElementById("fileName").value.split(".")[1]))) {
        let codeContent = editor.getSession().getValue();

        let validFileExtensionDict = {"py":"python", "java":"java", "c":"c","cpp":"cpp"};

        //console.log(validFileExtensionDict[document.getElementById("fileName").value.split(".")[1]]);

        if (validFileExtensionDict[document.getElementById("fileName").value.split(".")[1]] != currentLanguage && document.getElementById("fileName").value.split(".")[1] != undefined) {
            alert("Filename extension and language extension are inconsistant");
        }
        else {
            //console.log(document.getElementById("fileName").value.split(".")[0]);
            $.ajax({
                type: "POST",
                url: "/runSandbox",
                headers: {"language": currentLanguage, "fileName": document.getElementById("fileName").value.split(".")[0]},
                data: codeContent,
                success: function(response) {
                    var temp = response;
                    var count = (temp.match(/\/n/g) || []).length;
                    //console.log(count);
                    document.getElementById("codeExecutionOutput").innerHTML += response.replaceAll("/n","<br>");
                    var element = document.getElementById("codeExecutionOutputWrapper");
                    element.scrollTop = element.scrollHeight;
                    //document.getElementById("codeExecutionOutputWrapper").scrollTop = document.getElementById("codeExecutionOutputWrapper").scrollHeight;  
                //$("#codeExecutionOutput").html(response);
                //document.getElementById("place_for_suggestions").value = "hi";
                }
            });
        }
    }

      
      //scrollTop = element.scrollHeight;
      
}

function changeLanguage() {

    function IsNullOrWhiteSpace( value) {
        if (value== null){
            return true;
        } 
        return value.replace(/\s/g, '').length == 0;
    }
    function IsHelloWorld( value ) {
        if (value == `#include <iostream> \nint main()\n{\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}`) {
            return true;
        }
        if (value == `#include <stdio.h>\nint main() \n{\n    printf("Hello, World!");\n    return 0;\n}`) {
            return true;
        }
        if (value == `if __name__ == "__main__":\n    print("Hello, World!")`) {
            return true;
        }
        if (value == `class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}`) {
            return true;
        }
        return false;
    }

    currentLanguage =  document.getElementById("languageSelector").value
    if (currentLanguage == "cpp") {
        editor.session.setMode("ace/mode/c_cpp");
        
        if (IsNullOrWhiteSpace(editor.getValue()) || IsHelloWorld(editor.getValue())) {
            editor.setValue(`#include <iostream> \nint main()\n{\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}`);
        }
    }
    if (currentLanguage == "c") {
        editor.session.setMode("ace/mode/c_cpp");
        //console.log(IsHelloWorld(editor.getValue()));
        if (IsNullOrWhiteSpace(editor.getValue()) || IsHelloWorld(editor.getValue())) {
            editor.setValue(`#include <stdio.h>\nint main() \n{\n    printf("Hello, World!");\n    return 0;\n}`);
        }
    }
    if (currentLanguage == "python") {
        editor.session.setMode("ace/mode/python");
        if (IsNullOrWhiteSpace(editor.getValue()) || IsHelloWorld(editor.getValue())) {
            editor.setValue(`if __name__ == "__main__":\n    print("Hello, World!")`);
        }
    }
    if (currentLanguage == "java") {
        editor.session.setMode("ace/mode/java");

        if (IsNullOrWhiteSpace(editor.getValue()) || IsHelloWorld(editor.getValue())) {
            editor.setValue(`class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}`);
        }
    }

    
    if (document.getElementById("fileName").value.split(".")[0] == "Main" || document.getElementById("fileName").value.split(".")[0] == "main") {
        if (currentLanguage == "java") {
            document.getElementById("fileName").value = "Main.java"
        }
        if (currentLanguage == "c") {
            document.getElementById("fileName").value = "Main.c"
        }
        if (currentLanguage == "cpp") {
            document.getElementById("fileName").value = "Main.cpp"
        }
        if (currentLanguage == "python") {
            document.getElementById("fileName").value = "Main.py"
        }
    }

}

function clearCodeOutput() {
    document.getElementById("codeExecutionOutput").innerHTML = "";
}

function update() {
    //update the height of the editor because the percent sign doesn't work for some reason
    document.getElementById("editor").style.height = (window.innerHeight*0.66).toString() + "px";
    editor.resize();

    //update the output size
    document.getElementById("codeExecutionOutputWrapper").style.height = (window.innerHeight-28-28-28-(window.innerHeight*0.66)).toString() + "px";


    //File name changing
    let fileName = document.getElementById("fileName").value.split(".")[0];
    let fileExtension = document.getElementById("fileName").value.split(".")[1];

    let newWarning = "";

    var format = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
    if (format.test(fileName) && fileExtension != "") {
        newWarning += "File name cannot contain special characters";
    }

    let validFileExtensions = ["java", "py", "cpp", "c"]

    if (!(validFileExtensions.includes(fileExtension)) && fileExtension != ("" || undefined) ) {
        if (newWarning != "") {
            newWarning += " & ";
        }
        newWarning += "Unrecognized file extension";
    }
    document.getElementById("fileNameAlert").innerHTML = newWarning;

}

updateDisplay = setInterval(update,10);