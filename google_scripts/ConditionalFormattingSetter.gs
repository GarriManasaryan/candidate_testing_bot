function setConditionalFormatting() {

  // Define an array of sheet_names to skip
  var exception_list = ['Contents']
  var list_of_sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();

  // Iterate over every sheet (object) and apply conditional formatting rules
  for (const local_sheet of list_of_sheets){

    // Skip exception sheets
    if (!(exception_list.includes(local_sheet.getSheetName()))){

      // Remove all already existing conditional formatting rules
      local_sheet.setConditionalFormatRules([]);

      // Build new rules
      var conditionalFormatRules = local_sheet.getConditionalFormatRules();
      conditionalFormatRules.push(SpreadsheetApp.newConditionalFormatRule()
      .setRanges([local_sheet.getRange("A1:M")])
      .whenFormulaSatisfied('=AND($L1=False,NOT($L1=""))')
      .setBackground('#F4CCCC')
      .setFontColor('#660000')
      .build());

      conditionalFormatRules.push(SpreadsheetApp.newConditionalFormatRule()
      .setRanges([local_sheet.getRange("A1:M")])
      .whenFormulaSatisfied('=$L1')
      .setBackground('#D6FFDB')
      .setFontColor('#274E13')
      .build());

      // Set new rules to iterating sheet
      local_sheet.setConditionalFormatRules(conditionalFormatRules);
    }
  }
}
