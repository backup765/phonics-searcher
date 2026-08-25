
/*****
 * Open a new Google Sheet.
 * In the top menu, go to Extensions > Apps Script.
 * Replace any code in the editor with the following:
 * 
 * Click Deploy > New deployment.
 * Select Type: Web app.
 * Configure the settings:
    Execute as: Me
    Who has access: Anyone (Crucial: allows Carrd visitors to post data without logging into Google)
 * Click Deploy, authorize permissions when prompted, and copy the Web App URL.
 */
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var data = JSON.parse(e.postData.contents);
    
    // Appends [Timestamp, Word, Pronunciation] as a new row
    sheet.appendRow([new Date(), data.word, data.pronunciation]);
    
    return ContentService
      .createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}