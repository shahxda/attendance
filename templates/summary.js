function getAttendanceSummary(studentID) {
  // Retrieve attendance data from localStorage based on the student ID
  var attendanceData = JSON.parse(localStorage.getItem(studentID));

  var attendanceSummary = document.getElementById('attendanceSummary');

  if (attendanceData) {
    var summaryContent = "<h1>Attendance Summary for Student ID: " + studentID + "</h1>";
    summaryContent += "<table>";
    summaryContent += "<tr><th>Date</th><th>Time</th></tr>";

    for (var i = 0; i < attendanceData.length; i++) {
      summaryContent += "<tr>";
      summaryContent += "<td>" + attendanceData[i].date + "</td>";
      summaryContent += "<td>" + attendanceData[i].time + "</td>";
      summaryContent += "</tr>";
    }

    summaryContent += "</table>";
    attendanceSummary.innerHTML = summaryContent;
  } else {
    attendanceSummary.innerHTML = "No attendance data found for the provided student ID.";
  }
}

// Retrieve the student ID from the URL query parameter
var urlParams = new URLSearchParams(window.location.search);
var studentID = urlParams.get('id');

// Call the function to fetch and display attendance data
getAttendanceSummary(studentID);
