/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        read: function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/habits',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }       
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $name = $('#name'),
        $period = $('#period'),
        $goal = $('#goal');

    // return the API
    return {
        reset: function() {
            $name.val('');
            $period.val('').focus();
            $goal.val('');
        },
        update_editor: function(name, period, goal) {
            $name.val(name);
            $period.val(period).focus();
            $goal.val(goal);
        },
        build_table: function(habits) {
            let rows = ''

            // clear the table
            $('.habits table > tbody').empty();

            // did we get a people array?
            if (habits) {
                for (let i=0, l=habits.length; i < l; i++) {
                    rows += `<tr>
                                <td class="name">${habits[i].name}</td>
                                <td class="period">${habits[i].period}</td>
                                <td class="goal">${habits[i].goal}</td>
                             </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $name = $('#name'),
        $period = $('#period'),
        $goal = $('#goal');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(name, period, goal) {
        return name !== "" && period !== "" && goal !== "";
    }    

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            fname,
            lname;

        name = $target
            .parent()
            .find('td.name')
            .text();

        lname = $target
            .parent()
            .find('td.lname')
            .text();

        view.update_editor(fname, lname);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        console.log('arrombado')
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));