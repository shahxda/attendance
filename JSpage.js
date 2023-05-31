function checkAttendance() {
  var studentID = document.getElementById("studentID").value;
  var ip = getClientIP();

  if (localStorage.getItem(ip)) {
    alert("Error: Attendance already submitted from this IP address.");
    return;
  }

  localStorage.setItem(ip, true);

  // Process the attendance submission and display the submission time
  var submissionTime = new Date().toLocaleTimeString();
  alert(
    "Attendance submitted successfully. Submission time: " + submissionTime
  );

  // You can perform additional actions here, such as sending the data to a server using AJAX.
}

function getClientIP() {
  // Make an HTTP request to a public IP detection service
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "https://api.ipify.org?format=json", false);
  xhr.send();

  var response = JSON.parse(xhr.responseText);
  return response.ip;
}
