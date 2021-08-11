var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");
editor.setShowPrintMargin(false);

var currentLanguage = "python"

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
    currentLanguage =  document.getElementById("languageSelector").value
    if (currentLanguage == "cpp") {
        editor.session.setMode("ace/mode/c_cpp");
    }
    if (currentLanguage == "c") {
        editor.session.setMode("ace/mode/c_cpp");
    }
    if (currentLanguage == "python") {
        editor.session.setMode("ace/mode/python");
    }
    if (currentLanguage == "java") {
        editor.session.setMode("ace/mode/java");
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