function getAttendanceSummary(studentID) {
  // Retrieve attendance data from localStorage based on the student ID
  var attendanceData = JSON.parse(localStorage.getItem(studentID));

  var attendanceSummary = document.getElementById('attendanceSummary');

  if (attendanceData) {
    var summaryContent = "<h1>Attendance Summary</h1>";
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

document.addEventListener("DOMContentLoaded", function() {
  var submitButton = document.getElementById('submitAttendance');

  submitButton.addEventListener("click", function() {
    var studentID = document.getElementById('studentID').value;

    // Retrieve attendance data from localStorage based on the student ID
    var attendanceData = JSON.parse(localStorage.getItem(studentID)) || [];

    // Get the current date and time
    var currentDate = new Date();
    var submissionDate = currentDate.toLocaleDateString();
    var submissionTime = currentDate.toLocaleTimeString();

    // Create an attendance record
    var attendanceRecord = {
      date: submissionDate,
      time: submissionTime
    };

    // Add the attendance record to the attendanceData array
    attendanceData.push(attendanceRecord);

    // Store the updated attendance data in localStorage
    localStorage.setItem(studentID, JSON.stringify(attendanceData));

    // Redirect to the summary page with the student ID as a parameter
    window.location.href = "templates/summary.html" + encodeURIComponent(studentID);
  });
});
