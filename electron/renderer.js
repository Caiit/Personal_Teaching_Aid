const zerorpc = require("zerorpc");
let client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:3006");

client.invoke("echo", "server ready", (error, res) => {
  if (error || res !== 'server ready') {
    console.error(error);
  } else {
    console.log("server is ready");
  }
})

let start = document.getElementById("start")
let name = document.querySelector("#name");
let ip = "10.42.0.180" // TODO: deze moet variable
// Recognize student
start.addEventListener("click", () => {
  client.invoke("recognizeStudent", ip, (error, result) => {
    if (error) {
      console.error(error);
    } else if (result == "") {
      // Show input field
      document.getElementById("newStudentText").style.display = "block";
      document.getElementById("newStudent").style.display = "block";
      // start.style.display = "none";
    } else {
      // Show name
      name.textContent = result;
      document.getElementById("newStudent").style.display = "none";
      // start.style.display = "none";
      getProblems();
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
  getProblems();
})

// Get problems
function getProblems() {
  client.invoke("getNewProblem", (error, problem) => {
    if (error) {
      console.error(error);
    } else if (problem == "None") {
      document.getElementById("done").textContent = "You are finished.";
      answer.style.display = "none";
      document.getElementById("inputAnswer").style.display = "none";
    } else {
      document.getElementById("problem").textContent = problem;
      document.getElementById("problemPart").style.display = "inline-block";
    }
  })
}

// Handle answer
let nextProblem = document.querySelector("#nextProblem")
let answer = document.querySelector("#submitAnswer")
answer.addEventListener("click", () => {
  client.invoke("checkAnswer", (error, answeredCorrectly) => {
    if (error) {
      console.error(error);
    }
    // TODO: hier wat mee doen
    if (answeredCorrectly) {
      nextProblem.disabled = false;
      showImages(answeredCorrectly);
    } else {
      nextProblem.disabled = false;
      showImages(answeredCorrectly);
    }
  })
})

// Show an image that indicates whether the student answered correctly
function showImages(answeredCorrectly) {
  if (answeredCorrectly) {
    document.getElementById("correctImg").style.display = "inline-block";
  } else {
    document.getElementById("wrongImg").style.display = "inline-block";
  }
}

// Go to the next problem
nextProblem.addEventListener("click", () => {
  getProblems();
  nextProblem.disabled = true;
  document.getElementById("wrongImg").style.display = "none";
  document.getElementById("correctImg").style.display = "none";
})

// // Handle answer (CAITLIN MET INPUT VIA TEXT)
// let answer = document.querySelector("#submitAnswer")
// answer.addEventListener("click", () => {
//   var answer = document.getElementById("inputAnswer").value;
//   client.invoke("checkAnswer", answer, (error, result) => {
//     console.log(result)
//     if (error) {
//       console.error(error);
//     }
//     // TODO: hier wat mee doen
//     if (result) {
//       document.getElementById("problemPart").style.backgroundColor = "green";
//     } else {
//       document.getElementById("problemPart").style.backgroundColor = "red";
//     }
//   })
//   getProblems();
// })
