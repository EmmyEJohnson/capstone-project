$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutoComplete)
})

let autocomplete;

function initAutoComplete(){
   autocomplete = new google.maps.places.Autocomplete(
       document.getElementById('id-google-address'),
       {
           types: ['address'],
           componentRestrictions: {'country': [base_country.toLowerCase()]},
       })

   autocomplete.addListener('place_changed', onPlaceChanged);
}


function onPlaceChanged (){

    let place = autocomplete.getPlace();

    let geocoder = new google.maps.Geocoder()
    let address = document.getElementById('id-google-address').value

    geocoder.geocode( { 'address': address}, function(results, status) {

        if (status == google.maps.GeocoderStatus.OK) {
            let latitude = results[0].geometry.location.lat();
            let longitude = results[0].geometry.location.lng();

            $('#id_longitude').val(longitude) 
            $('#id_latitude').val(latitude) 
        } 
    }); 

    if (!place.geometry){
        document.getElementById('id-google-address').placeholder = "*Begin typing address";
    }
    else{
        
        for (let i = 0; i < place.address_components.length; i++) {
            for (let j = 0; j < place.address_components[i].types.length; j++) {

                if (place.address_components[i].types[j] == "street_number") {
                    let num = place.address_components[i].long_name  
                }
                if (place.address_components[i].types[j] == "route") {
                    let addy = place.address_components[i].long_name
                }
                if (place.address_components[i].types[j] == "city") {
                     $('#id_city').val(place.address_components[i].long_name)   
                }                    
                if (place.address_components[i].types[j] == "administrative_area_level_2") {
                    $('#id_state').val(place.address_components[i].long_name)   
                }
                if (place.address_components[i].types[j] == "country") {
                    $('#id_country').val(place.address_components[i].long_name)   
                }

                if (place.address_components[i].types[j] == "zip_code") {
                    $('#id_zip_code').val(place.address_components[i].long_name)   
                }
            }
        }
        $('#id_address').val(num + " " + addy)

        //find all hidden inputs & ignore csrf token
        let x = $( "input:hidden" );
        for (let i = 0; i < x.length; i++){
            if (x[i].name != "csrfmiddlewaretoken")  
            x[i].type = "text"; 
            x.eq(x).attr("class", 'hidden-el')  
        }

        //fade in the completed form
        $('.hidden-el').fadeIn()
        $('#profile-btn').removeAttr("disabled")
    }
}