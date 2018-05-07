
// Create a new XMLHttpRequest.
var request = new XMLHttpRequest();

// Handle state changes for the request.
request.onreadystatechange = function(response) {
  if (request.readyState === 4) {
    if (request.status === 200) {
      // Get the <datalist> and <input> elements.
      var dataList = document.getElementById('json-datalist');
      var input = document.getElementById('name');

      // Parse the JSON
      var jsonOptions = JSON.parse(request.responseText);
  
      // Loop over the JSON array.
      jsonOptions.forEach(function(item) {
        // Create a new <option> element.
        var option = document.createElement('option');
        // Set the value using the item in the JSON array.
        option.value = item;
        // Add the <option> element to the <datalist>.
        dataList.appendChild(option);
      });
      
      // Update the placeholder text.
      input.placeholder = "Search for your name";
    } else {
      // An error occured :(
      input.placeholder = "Couldn't load suggestions :(";
    }
  }
};

// Update the placeholder text.
// input.placeholder = "Loading options...";

// Set up and make the request.
request.open('GET', 'http://ec2-18-144-6-174.us-west-1.compute.amazonaws.com:5000/all_names', true);
request.send();
