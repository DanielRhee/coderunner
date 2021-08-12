var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");
editor.setShowPrintMargin(false);

var currentLanguage = "python"

function startEnvironment() {
    changeLanguage();
}

function executeCode() {
    let codeContent = editor.getSession().getValue();

      $.ajax({
        type: "POST",
        url: "/runSandbox",
        headers: {"language": currentLanguage},
        data: codeContent,
        success: function(response) {
            var temp = response;
            var count = (temp.match(/\/n/g) || []).length;
            console.log(count);
            document.getElementById("codeExecutionOutput").innerHTML += response.replaceAll("/n","<br>");
            var element = document.getElementById("codeExecutionOutputWrapper");
            element.scrollTop = element.scrollHeight;
            //document.getElementById("codeExecutionOutputWrapper").scrollTop = document.getElementById("codeExecutionOutputWrapper").scrollHeight;  
          //$("#codeExecutionOutput").html(response);
          //document.getElementById("place_for_suggestions").value = "hi";
        }
      });

      
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
        if (IsNullOrWhiteSpace(editor.getValue()) || IsHelloWorld(editor.getValue())) {
            editor.setValue(`#include <stdio.h>\nint main() \n{\n    printf("Hello World!");\n    return 0;\n}`);
        }
    }
    if (currentLanguage == "python") {
        editor.session.setMode("ace/mode/python");
        if (IsNullOrWhiteSpace(editor.getValue()) || IsHelloWorld(editor.getValue())) {
            editor.setValue(`if __name__ == "__main__":\n    print("hello")`);
        }
    }
    if (currentLanguage == "java") {
        editor.session.setMode("ace/mode/java");

        if (IsNullOrWhiteSpace(editor.getValue()) || IsHelloWorld(editor.getValue())) {
            editor.setValue(`class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}`);
        }
    }
}

function update() {
    //update the height of the editor because the percent sign doesn't work for some reason
    document.getElementById("editor").style.height = (window.innerHeight*0.66).toString() + "px";
    editor.resize();

    //update the output size
    document.getElementById("codeExecutionOutputWrapper").style.height = (window.innerHeight-28-28-28-(window.innerHeight*0.66)).toString() + "px";
}

updateDisplay = setInterval(update,10);