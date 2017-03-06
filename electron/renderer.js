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
      document.getElementById("nextProblem").style.display = "none";
    } else {
      document.getElementById("problem").textContent = problem;
      document.getElementById("problemPart").style.display = "inline-block";
    }
  })
}

// Get student's response
let answer = document.querySelector("#submitAnswer");
answer.addEventListener("click", () => {
  var displayValue = inputAnswer.style.display;

  if (displayValue !== "none" && displayValue !== "")  {
    var givenAnswer = document.getElementById("giveAnswer").value;
    checkAnswer(givenAnswer);
  } else {
    getResponse();
  }
})

let inputAnswer = document.querySelector("#inputAnswer");
function getResponse() {
  client.invoke("getResponse", (error, response) => {
    if (error) {
      console.error(error);
      inputAnswer.style.display = "block";
      textToSpeech("Ik heb je niet begrepen");
    } else if (response !== "Ik heb je niet begrepen" && response != null) {
        checkAnswer(response)
    } else {
      textToSpeech(response);
      inputAnswer.style.display = "block";
    }
  })
}

// Convert a string to speech that is said out loud
function textToSpeech(string) {
  client.invoke("textToSpeech", string, (error) => {
    if (error) {
      console.error(error);
    }
  })
}

// Handle student's response
let nextProblem = document.querySelector("#nextProblem");
function checkAnswer(response) {
  client.invoke("checkAnswer", response, (error, result) => {
    document.getElementById("correctImg").style.display = "none";
    document.getElementById("wrongImg").style.display = "none";

    if (error) {
      console.error(error);
    } else {
      var answeredCorrectly = result[0];
      var message = result[1];

      nextProblem.disabled = false;
      showImages(answeredCorrectly);
      textToSpeech(message);
    }
  })
}

// Show an image that indicates whether the student answered correctly
function showImages(answeredCorrectly) {
  if (answeredCorrectly) {
    document.getElementById("correctImg").style.display = "inline-block";
  } else {
    document.getElementById("wrongImg").style.display = "inline-block";
    inputAnswer.style.display = "block";
  }
}

// Go to the next problem
nextProblem.addEventListener("click", () => {
  getProblems();
  nextProblem.disabled = true;
  document.getElementById("wrongImg").style.display = "none";
  document.getElementById("correctImg").style.display = "none";
  inputAnswer.reset();
  inputAnswer.style.display = "none"
})
