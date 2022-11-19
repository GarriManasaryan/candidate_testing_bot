function onOpen() {
  SpreadsheetApp.getUi().createMenu('✔️ Generate token')
    .addItem('Run', 'generateTokenPerCandidate')
    .addToUi();
}

function generateTokenPerCandidate(){
  var ui = SpreadsheetApp.getUi()
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Candidates")
  var table_values = sheet.getDataRange().getValues()
  var all_tokens = table_values.map(x => {return x[0]})

  for (var i = 0 ; i<table_values.length ; i++){
    if (!(table_values[i][0].toString().length > 0)){

      var first_name = table_values[i][2].toString().toLowerCase().replaceAll(' ', '')
      var last_name = table_values[i][3].toString().toLowerCase().replaceAll(' ', '')

      if (first_name == '' || last_name == ''){
        ui.alert('⚠️ Validation failed ⚠️' , `Both first and last names should be specified, please fill the data and try again`, ui.ButtonSet.OK)

      }

      else{
        // validate docx id for download
        var status = validateDocxID(table_values[i][6])

        if (!(status)){
          ui.alert('⚠️ Validation of Task.docx failed ⚠️' , `Please check the link to docx task for ${first_name} ${last_name} and generate the token again`, ui.ButtonSet.OK)
        }

        else{

          // generate token
          var token = genToken(first_name, last_name)
          while (all_tokens.includes(token)){
            token = genToken(first_name, last_name)
          }

          sheet.getRange(`A${i+1}`).setValue(token)

        }
      }

    }
  }

}

function genToken(first_name, last_name) {

  var f_name = first_name.length > 2 && first_name != '' ? first_name.slice(0,2) : "nm"
  var l_name = last_name.length > 2 && last_name != '' ? last_name.slice(0,2) : "lm"

  var uuid_full = Utilities.getUuid()
  var uuid_first_chunk = uuid_full.slice(0,8)
  var uuid_last_chunk = uuid_full.slice(19,)
  var token = ['cand', f_name, uuid_first_chunk, l_name, uuid_last_chunk].join('-')
  return token

}

function validateDocxID(link_to_docx){
  try{
    var doc_id = link_to_docx.replaceAll(' ', '').split("/")[5]
    var valid_doc_id = doc_id.length == 44 ? true : false
  }
  catch{
    var valid_doc_id = false

  }

  return valid_doc_id

}

function set_new_conditional_form_rules() {

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
