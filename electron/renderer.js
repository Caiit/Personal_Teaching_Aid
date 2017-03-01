const zerorpc = require("zerorpc");
let client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:3006");

var studentId;

client.invoke("echo", "server ready", (error, res) => {
  if (error || res !== 'server ready') {
    console.error(error);
  } else {
    console.log("server is ready");
  }
})

let start = document.getElementById("start");
let name = document.querySelector("#name");

// Recognize student
start.addEventListener("click", () => {
  client.invoke("recognizeStudent", (error, result) => {
    var id = result[0];
    var studentName = result[1];
    if (error) {
      console.error(error);
    } else if (id == "_unknown") {
      // Show input field
      // name.textContent = "";
      document.getElementById("newStudent").style.display = "block";
    } else {
      // Show name
      studentId = id;
      name.textContent = studentName;
      document.getElementById("newStudent").style.display = "none";
      getProblems(studentId);
    }
  })
})


// Add new user
let newUser = document.querySelector("#submitNewStudent")
newUser.addEventListener("click", () => {
  var form = document.getElementById("newStudentForm");
  var fName = form.elements[0].value;
  var lName = form.elements[1].value;

  client.invoke("addNewUser", fName, lName, (error) => {
    if (error) {
      console.error(error);
    }
    // Show name
    name.textContent = fName + " " + lName;
    document.getElementById("newStudent").style.display = "none";
  })
})

// Get problems
function getProblems(studentId) {
  client.invoke("getNewProblem", (error, problem) => {
    if (error) {
      console.error(error);
    } else {
      document.getElementById("problem").textContent = problem;
    }
  })
}
