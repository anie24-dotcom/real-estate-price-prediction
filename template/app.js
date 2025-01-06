
function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for (var i = 0; i < uiBathrooms.length; i++) {
        if (uiBathrooms[i].checked) {
            return parseInt(uiBathrooms[i].value);
        }
    }
    return -1; // Invalid Value
}

function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for (var i = 0; i < uiBHK.length; i++) {
        if (uiBHK[i].checked) {
            return parseInt(uiBHK[i].value);
        }
    }
    return -1; // Invalid Value
}

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");

    var url = "http://127.0.0.1:5000/api/predict_home_price"; // Correct API endpoint
    // Prepare the payload
    var payload = {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    };

    // Send a POST request to the backend with the form data
    $.ajax({
        url: url,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(payload),
        success: function (data) {
            console.log("Response:", data.estimated_price);
            estPrice.innerHTML = "<h2>Estimated Price: ₹" + data.estimated_price.toFixed(2) + "</h2>";
        },
        error: function (error) {
            console.error("Error:", error);
            alert("Something went wrong. Please try again!");
        }
    });
}

function onPageLoad() {
    console.log("document loaded");
    var url = "http://127.0.0.1:5000/api/get_location_names"; // Correct API endpoint

    // Fetch available locations from the backend
    $.get(url, function (data, status) {
        console.log("got response for get_location_names request");
        if (data && data.locations) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");

            // Clear existing options and populate new ones
            $('#uiLocations').empty();
            $('#uiLocations').append(new Option("Choose a Location", "", true, true));
            for (var i = 0; i < locations.length; i++) {
                var opt = new Option(locations[i], locations[i]); // Add value attribute to options
                $('#uiLocations').append(opt);
            }
        } else {
            alert("Failed to load locations");
        }
    }).fail(function (error) {
        console.error("Error fetching location names from the backend:", error);
        alert("Error fetching location names. Please try again.");
    });
}

// Trigger the onPageLoad function when the window is loaded
window.onload = onPageLoad;
