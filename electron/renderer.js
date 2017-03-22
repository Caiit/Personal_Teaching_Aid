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

// let start = document.getElementById("start");
let name = document.querySelector("#name");
// // Recognize student
// start.addEventListener("click", () => {
//   client.invoke("recognizeStudent", "None", (error, result) => {
//     if (error) {
//       console.error(error);
//     } else if (result == "") {
//       // Show input field
//       document.getElementById("newStudentText").style.display = "block";
//       document.getElementById("newStudent").style.display = "block";
//       hideStartButtons();
//     } else {
//       // Show name
//       name.textContent = result;
//       document.getElementById("newStudent").style.display = "none";
//       hideStartButtons();
//       getProblems();
//     }
//   })
// })

let naoProgram = document.getElementById("naoImg");
naoProgram.addEventListener("click", () => {
  getIpAddress();
})

let cancelNaoProgram = document.getElementById("cancelIp");
cancelNaoProgram.addEventListener("click", () => {
  document.getElementById("askNaoContainer").style.display = "block";
  document.getElementById("getIp").style.display = "none";
})

// Use an input field to get the robot's IP address
function getIpAddress() {
  document.getElementById("askNaoContainer").style.display = "none";
  document.getElementById("getIp").style.display = "block";

  document.getElementById("giveIp").addEventListener("click", () => {
    ip = document.getElementById("inputIp").value;

    if (ip != null && ip !== "") {
      document.getElementById("getIp").style.display = "none";
      startProgram(ip);
    }
  })
}

let noNaoProgram = document.getElementById("noNaoImg");
noNaoProgram.addEventListener("click", () => {
  startProgram("None");
})

function startProgram(ip) {
  client.invoke("startProgram", ip, (error, result) => {
    if (error) {
      console.error(error);
    } else if (result == "") {
      // Show input field
      document.getElementById("newStudent").style.display = "block";
      document.getElementById("startUpScreen").style.display = "none";
      textToSpeech("Ik ken je nog niet. Wie ben je?")
    } else {
      // Show name
      name.textContent = result;
      document.getElementById("newStudent").style.display = "none";
      document.getElementById("startUpScreen").style.display = "none";
      getProblems();
    }
  })
}

// Get problems
function getProblems() {
  document.getElementById("name").style.display = "block";
  client.invoke("getNewProblem", (error, problem) => {
    if (error) {
      console.error(error);
    } else if (problem == "None") {
        document.getElementById("problemContainer").style.display = "none";
        document.getElementById("endScreen").style.display = "block";
        endProgram();
    } else {
      document.getElementById("problem").textContent = problem;
      document.getElementById("problemContainer").style.display = "inline-block";
    }
  })
}

// Ends the program
function endProgram() {
  client.invoke("endProgram", (error) => {
    if (error) {
      console.log(error);
    }
  })
}

// Add new user
let newUser = document.querySelector("#submitNewStudent")
newUser.addEventListener("click", () => {
  var form = document.getElementById("newStudentForm");
  var fName = form.elements[0].value;
  var lName = form.elements[1].value;

  client.invoke("addNewUser", fName, lName, (error) => {
    if (error) {
      console.error(error);
    } else {
      // Show name
      name.textContent = fName + " " + lName;
      document.getElementById("newStudent").style.display = "none";
      getProblems();
    }
  })
})

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
  var listeningImg = document.getElementById("listeningImg")
  listeningImg.style.display = "block";

  client.invoke("getResponse", (error, response) => {
    if (error) {
      listeningImg.style.display = "none";
      console.error(error);
      inputAnswer.style.display = "block";
    } else if (response != "Ik heb je niet begrepen" &&
      response != "Ik kon je niet verstaan" && response != null) {
        listeningImg.style.display = "none";
        checkAnswer(response);
    } else {
      listeningImg.style.display = "none";
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
      textToSpeech(message);

      if (message != "Je twijfelde") {
        showImages(answeredCorrectly);
      } else {
        getProblems();
      }
      nextProblem.disabled = false;
    }
  })
}

// Show an image that indicates whether the student answered correctly
function showImages(answeredCorrectly) {
  if (answeredCorrectly) {
    document.getElementById("correctImg").style.display = "inline-block";
    document.getElementById("submitAnswer").disabled = true;
  } else {
    document.getElementById("wrongImg").style.display = "inline-block";
    inputAnswer.style.display = "block";
  }
}

// Go to the next problem
nextProblem.addEventListener("click", () => {
  getProblems();
  nextProblem.disabled = true;
  document.getElementById("submitAnswer").disabled = false;
  document.getElementById("wrongImg").style.display = "none";
  document.getElementById("correctImg").style.display = "none";
  inputAnswer.reset();
  inputAnswer.style.display = "none"
})

// Restart the program
let restartButton = document.querySelector("#restart");
restartButton.addEventListener("click", () => {
  document.getElementById("endScreen").style.display = "none";
  document.getElementById("startUpScreen").style.display = "block";
  document.getElementById("name").style.display = "none";
})
