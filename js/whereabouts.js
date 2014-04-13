var presence_map = {}

function display_person (uniqname) {
    // Get location string
    var loc = presence_map[uniqname][0];
    loc = loc.replace(/[\|]+/g, ", ").replace("|", ", ");
    
    // Get time string
    var time = new Date(presence_map[uniqname][1]);
    var hours = time.getHours();
    var minutes = time.getMinutes();
    var suffex = (hours >= 12)? 'PM' : 'AM';
    hours = (hours > 12)? hours-12 : hours;
    hours = (hours == '00')? 12 : hours;
    minutes = (minutes < 10)? '0'+minutes : minutes;
    time = hours.toString() + ":" + minutes.toString() + " " + suffex;

    // Get full name
    var full_name = presence_map[uniqname][2];

    // Get picture location
    var pic_src = "http://lab11.eecs.umich.edu/content/people/images/" + uniqname

    // Try picture as a jpg
    var new_entry = 
        $('<div class="col-lg-2">' +
          '<img class="img-circle" src="' + pic_src + '.jpg" height="140px">' +
          '<h3>' + full_name + '</h3>' +
          '<p>' + loc + '</p>' +
          '<p> Updated: ' + time + '</p>' +
          '</div>')
        .error(function() {
            // Try as a png
            $('<div class="col-lg-2">' +
              '<img class="img-circle" src="' + pic_src + '.png" height="140px">' +
              '<h3>' + full_name + '</h3>' +
              '<p>' + loc + '</p>' +
              '<p> Updated: ' + time + '</p>' +
              '</div>')
            .error(function() {
                // Default picture
                $('<div class="col-lg-2">' +
                  '<img class="img-circle" src="images/person-placeholder.jpg" height="140px">' +
                  '<h3>' + full_name + '</h3>' +
                  '<p>' + loc + '</p>' +
                  '<p> Updated: ' + time + '</p>' +
                  '</div>')
            });
        });
    
    $("#people_row").append(new_entry);
}

function record_presence (person_list, loc, time) {
    $("#people_row").empty();

    // Check if new people need to be added to the map
    for (var i=0; i<person_list.length; i++) {
        var person = person_list[i];
        var uniqname = Object.keys(person_list[i])[0];
        var full_name = person_list[i][uniqname];

        if (!(uniqname in presence_map)) {
            presence_map[uniqname] = [loc, time, full_name];
        }
    }

    // Iterate through map, updating and displaying
    //console.log("Presence Map Updated:");
    var present_uniqnames = Object.keys(presence_map).sort();
    for (var i=0; i<present_uniqnames.length; i++) {
        var present_uniqname = present_uniqnames[i];
        
        var present = false;
        for (var j=0; j<person_list.length; j++) {
            var uniqname = Object.keys(person_list[j])[0];
            var full_name = person_list[j][uniqname];
            
            if (uniqname == present_uniqname) {
                // Person is present, update entry and display
                present = true;
                presence_map[present_uniqname][0] = loc;
                presence_map[present_uniqname][1] = time;
                display_person(present_uniqname);
            }
        }

        if (!present) {
            if (presence_map[uniqname][0] == loc) {
                // Person no longer presesnt
                presence_map[present_uniqname][0] = "";
                presence_map[present_uniqname][1] = time;
            } else if (presence_map[present_uniqname][0] != "") {
                // Person still present somewhere else
                display_person(present_uniqname);
            }
        }

        //console.log("presence_map[" + present_uniqname + "]:");
        //console.log(presence_map[present_uniqname].toString());
    }

}

