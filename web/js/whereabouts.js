var presence_map = {}

function display_person (uniqname) {
    // Get location string
    var loc = presence_map[uniqname][0];
    loc = loc.replace(/[\|]+/g, ", ").replace("|", ", ");

    // Get since string
    var since = new Date(presence_map[uniqname][3]*1000);
    var hours = since.getHours();
    var minutes = since.getMinutes();
    var suffex = (hours >= 12)? 'PM' : 'AM';
    hours = (hours > 12)? hours-12 : hours;
    hours = (hours == '00')? 12 : hours;
    minutes = (minutes < 10)? '0'+minutes : minutes;
    since = hours.toString() + ":" + minutes.toString() + " " + suffex;
    since = "Since: " + since;

    // Get time string
    var time = new Date(presence_map[uniqname][1]);
    hours = time.getHours();
    minutes = time.getMinutes();
    suffex = (hours >= 12)? 'PM' : 'AM';
    hours = (hours > 12)? hours-12 : hours;
    hours = (hours == '00')? 12 : hours;
    minutes = (minutes < 10)? '0'+minutes : minutes;
    time = hours.toString() + ":" + minutes.toString() + " " + suffex;
    time = "Updated: " + time;

    // Get full name
    var full_name = presence_map[uniqname][2];

    // Update the entry
    $('#' + uniqname + '_name').text(full_name);
    $('#' + uniqname + '_loc').text(loc);
    $('#' + uniqname + '_since').text(since);
    $('#' + uniqname + '_time').text(time);

    // Make sure person is visable
    $('#' + uniqname).show();
    //console.log("Showing " + uniqname);
}

function hide_person (uniqname) {
    // Hide the person
    $('#' + uniqname).hide();
    //console.log("Hiding " + uniqname);
}


//XXX: This requires a good bit of thought to determine how to sort the people
function create_person (uniqname, full_name) {
    var loc = "None";
    var since = "0:00";
    var time = "0:00";

    // Create new div for content
    var new_entry = 
        $('<div class="col-lg-2" id="' + uniqname +'">' +
          '<div id="' + uniqname + '_img"></div>' +
          '<h3 id="' + uniqname + '_name">' + full_name + '</h3>' +
          '<p  id="' + uniqname + '_loc">' + loc + '</p>' +
          '<p  id="' + uniqname + '_since"> Since: ' + since + '</p>' +
          '<p  id="' + uniqname + '_time"> Updated: ' + time + '</p>' +
          '</div>');

    // Get picture location
    var pic_src = "http://lab11.eecs.umich.edu/content/people/images/" + uniqname;

    // Get picture
    // Goodness this is awful. Try website jpg, try website png, try local jpg, try local png, give up
    // Note that these are actually nested, but laying them out in line looks better
    var img = $('<img class="img-circle" height="140px"/>').attr('src', pic_src + '.jpg')
        .error( function() { /*console.log("Trying web png");*/   img.attr('src', pic_src + '.png')
        .error( function() { /*console.log("Trying local jpg");*/ img.attr('src', 'images/' + uniqname + '.jpg')
        .error( function() { /*console.log("Trying local png");*/ img.attr('src', 'images/' + uniqname + '.png')
        .error( function() { /*console.log("Placeholder");*/      img.attr('src', 'images/person-placeholder.jpg')
    ;});});});});

    // Actually add person to page. Need to sort by children full names
    if ($("#people_row").children().length > 0) {
        var child_list = $("#people_row").children();
        for (var i=0; i<child_list.length; i++) {
            var child_full_name = $("#" + child_list[i].id + "_name").text();
            if (child_full_name > full_name) {
                new_entry.insertBefore("#" + child_list[i].id);
                $('#' + uniqname + '_img').append(img);
                //console.log("Creating " + uniqname);
                return;
            }
        }
    }

    $("#people_row").append(new_entry);
    $('#' + uniqname + '_img').append(img);
    //console.log("Creating " + uniqname);
}

function record_presence (person_list, loc, time, since_list) {

    // Check if new people need to be added to the map
    for (var i=0; i<person_list.length; i++) {
        var uniqname = Object.keys(person_list[i])[0];

        if (!(uniqname in presence_map)) {
            var full_name = person_list[i][uniqname];
            var since = since_list[i][uniqname];
            presence_map[uniqname] = [loc, time, full_name, since];
            create_person(uniqname, full_name);
        }
    }

    // Iterate through map, updating and displaying
    //console.log("Presence Map Updated:");
    var anyone_here = false;
    var present_uniqnames = Object.keys(presence_map).sort();
    for (var i=0; i<present_uniqnames.length; i++) {
        var present_uniqname = present_uniqnames[i];

        var present = false;
        for (var j=0; j<person_list.length; j++) {
            var uniqname = Object.keys(person_list[j])[0];

            if (uniqname == present_uniqname) {
                var full_name = person_list[j][uniqname];
                var since = since_list[j][uniqname];

                // Person is present, update entry and display
                present = true;
                presence_map[present_uniqname][0] = loc;
                presence_map[present_uniqname][1] = time;
                presence_map[present_uniqname][2] = full_name;
                presence_map[present_uniqname][3] = since;
                display_person(present_uniqname);
                anyone_here = true;
            }
        }

        if (!present) {
            if (presence_map[present_uniqname][0] == loc) {
                // Person no longer present
                presence_map[present_uniqname][0] = "";
                presence_map[present_uniqname][1] = time;
                presence_map[present_uniqname][3] = 0;
                hide_person(present_uniqname);
            } else if (presence_map[present_uniqname][0] != "") {
                // Person still present somewhere else
                display_person(present_uniqname);
                anyone_here = true;
            }
        }

        //console.log("presence_map[" + present_uniqname + "]:");
        //console.log(presence_map[present_uniqname].toString());
    }

    // If no one was found, display a message
    if (!anyone_here) {
        $("#empty_text").show();
    } else {
        $("#empty_text").hide();
    }
}

