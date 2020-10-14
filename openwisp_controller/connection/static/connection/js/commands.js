'use strict';

const deviceId = getObjectIdFromUrl();
const commandWebSocket = new ReconnectingWebSocket(
    `${getWebSocketProtocol()}${location.host}/ws/device/${getObjectIdFromUrl()}/command`,
    null, {
        debug: false
    }
);

django.jQuery(function ($) {
    let selector = $('#id_command_set-0-type'),
        showFields = function () {
            var fields = $('#command_set-group fieldset > .form-row:not(.field-type):not(.field-params), .jsoneditor-wrapper'),
                value = selector.val();
            if (!value) {
                fields.hide();
            } else {
                $('#command_set-2-group fieldset .dynamic-command_set-2:first');
                fields.show();
            }
        };
    selector.change(function () {
        showFields();
    });

    $(document).one('jsonschema-schemaloaded', function () {
        showFields();

        initCommandDropdown($);
        initCommandOverlay($);
        initCommandWebSockets($);
    });
});


function initCommandDropdown($) {
    // Add "Send Command" widget
    $(function () {
        let widgetElement,
            objectTools = $('.object-tools'),
            owCommandBtns = '',
            schema = django._schemas[$('#id_command_set-0-input').data('schema-url')];

        // Don't add the widget if object tools are not enabled
        if (objectTools.length === 0) {
            return;
        }

        Object.keys(schema).forEach(function (el) {
            owCommandBtns +=
                `<button class="ow-command-btn" data-command="${el}">${schema[el].title}</button>`;
        });
        widgetElement = `
            <li>
                <a href="#" id="send-command">${gettext('Send Command')}</a>
                <div class="ow-device-command-option-container ow-hide">
                    ${owCommandBtns}
                </div>
            </li>`;
        $('.object-tools li+li').before(widgetElement);
    });

    // Only show "Send command" button when a device has credentials present
    $(function () {
        if ($('.dynamic-deviceconnection_set').length === 0) {
            $('#send-command').parent().addClass('ow-hide');
        }
    });

    $('.object-tools').on('click', '#send-command', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $('.ow-device-command-option-container').toggleClass('ow-hide');
    });

    $(document).click(function (e) {
        e.stopPropagation();
        // Check if the clicked area is dropDown or not
        if ($('.ow-device-command-option-container').has(e.target).length === 0) {
            hideDropdown();
        }
    });

    $('.object-tools').on('focusout', '.ow-device-command-option-container', function (e) {
        // Hide dropdown while accessing dropdown through keyboard
        e.stopPropagation();
        if ($('.ow-device-command-option-container').has(e.relatedTarget).length === 0) {
            hideDropdown();
        }
    });

    // Escape and enter key handlers for command dropdown
    $('.object-tools').on('keyup', '.ow-command-btn', function (e) {
        e.preventDefault();
        e.stopPropagation();
        // Close widget on escape key
        if (e.keyCode == 27) {
            hideDropdown();
        }

        // Open command overlay for selected command option
        if (e.keyCode == 13) {
            $(e.target).click();
        }
    });

    $('.object-tools').on('keyup', '#send-command', function (e) {
        e.preventDefault();
        e.stopPropagation();
        // Close widget on escape key
        if (e.keyCode == 27) {
            hideDropdown();
        }
    });

    $('.object-tools').on('click', '.ow-command-btn', function () {
        let commandType = $(this).data('command');
        $('#id_command_set-0-type').val(commandType);
        $('#id_command_set-0-type').trigger('change');

        let element = $('#id_command_set-0-input_jsoneditor .errorlist li:first-child'),
            schema = django._schemas[$('#id_command_set-0-input').data('schema-url')],
            message = schema[commandType].message;

        // execute command if no input required
        if (schema[commandType].type === 'null') {
            $('#ow-command-submit-btn').trigger('click');
            return;
        }

        // Set focus to input field inside overlay
        $('#command_set-group').css('display', 'block');
        $('html').css('overflow-y', 'hidden');
        $('#id_command_set-0-input_jsoneditor input.vTextField:visible:first').focus();
        $('#id_command_set-0-input_jsoneditor .form-row').removeClass('errors');

        // Update custom validation message on command form
        element.html(message);
    });

    function hideDropdown() {
        $('.ow-device-command-option-container').addClass('ow-hide');
    }
}

function initCommandOverlay($) {
    // Add close button on the overlay
    $(function () {
        let elements = `
            <p class="errornote ow-command-overlay-errornote ow-hide" id="ow-command-overlay-validation-error">Please correct the errors below.</p>
            <p class="errornote ow-command-overlay-errornote ow-hide" id="ow-command-overlay-request-error">An error encountered, please try sometime later.</p>
            <button id="ow-command-overlay-close"><img class="icon" src="/static/admin/img/icon-deletelink.svg"></button>`;
        $('#command_set-0 .form-row.field-input').prepend(elements);
    });

    // Add submit button on the overlay
    $(function () {
        let buttonElement = `
            <div class="ow-command-submit-btn-wrapper">
                <button class="button" id="ow-command-submit-btn">Execute Command</button>
            </div>`;
        $('#command_set-0 > fieldset').append(buttonElement);
    });

    // Close overlay on clicking on blurred space
    $('#command_set-group').click(function (e) {
        if ($('#command_set-group > fieldset').has(e.target).length === 0) {
            closeOverlay();
        }
    });

    // Close overlay on clicking close button
    $('#command_set-group').on('click', '#ow-command-overlay-close', function (e) {
        e.preventDefault();
        closeOverlay();
        resetCommandForm();
    });

    function checkInputIsValid() {
        // Remove all error messages
        $('#id_command_set-0-input_jsoneditor .errorlist').removeClass('ow-command-errorlist');

        let jsonEditor = django._jsonEditors['id_command_set-0-input_jsoneditor'],
            errors = jsonEditor.validate();
        if (errors.length) {
            // Show error only for input fields having error
            errors.forEach(function (el) {
                let inputName = el.path.replace('.', '[') + ']',
                    element = $(`#id_command_set-0-input_jsoneditor input[name="${inputName}"]`),
                    errorList = element.next();
                errorList.addClass('ow-command-errorlist');
            });
            $('#ow-command-overlay-validation-error').removeClass('ow-hide');
            return false;
        }
        // hide errors
        $('#id_command_set-0-input_jsoneditor .errorlist').hide();
        $('#ow-command-overlay-validation-error').addClass('ow-hide');
        return true;
    }

    // Click handler for execute button
    $('#command_set-group').on('click', '#ow-command-submit-btn', function (e) {
        e.preventDefault();
        if (!checkInputIsValid()) {
            return;
        }
        let data = {
            "type": $('#id_command_set-0-type').val(),
            "input": $('#id_command_set-0-input').val()
        };
        $.ajax({
            type: 'POST',
            url: `/api/v1/device/${deviceId}/command/`,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            dataType: 'json',
            xhrFields: {
                withCredentials: true
            },
            data: data,
            crossDomain: true,
            beforeSend: function () {
                $('#loading-overlay').show();
            },
            complete: function () {
                if (!isRecentCommandsAbsent()) {
                    $('#loading-overlay').fadeOut(250);
                }
            },
            success: function (response) {
                closeOverlay();
                updateRecentCommands($, response);
                resetCommandForm();
                location.assign('#command_set-2-group');
            },
            error: function () {
                $('#ow-command-overlay-validation-error').addClass('ow-hide');
                $('#ow-command-overlay-request-error').removeClass('ow-hide');
            }
        });
    });

    // hitting enter in one of the input fields won't submit
    // the device form but will execute the command
    $('#command_set-group').on('keypress keyup keydown', '.jsoneditor-wrapper input', function (e) {
        if (e.keyCode === 13) {
            let execButton = $('#ow-command-submit-btn');
            // workaround to bug which prevents jsoneditor
            // from getting the updated value
            execButton.focus();
            $(e.target).focus();
            // submit only on keyup event
            if (e.type === 'keyup') {
                execButton.trigger('click');
            }
            // avoid form submit
            e.preventDefault();
            return false;
        }
    });

    // Hitting ESC key closes overlay
    $('body').keyup(function (e) {
        // Check if command overlay is visible or not
        if ($('#command_set-group:visible').length !== 0) {
            // Hide overlay on "Escape" key
            if (e.keyCode === 27) {
                closeOverlay();
            }
        }
    });

    function closeOverlay() {
        $('#id_command_set-0-type').val('reboot');
        $('#id_command_set-0-type').trigger('change');
        $('#command_set-group').css('display', 'none');
        $('.ow-command-overlay-errornote').addClass('ow-hide');
        $('html').css('overflow-y', '');
        // After closing the overaly, change focus to dropdown button
        $('#send-command').focus();
    }

    function resetCommandForm() {
        $('#id_command_set-0-type').val(null);
        $('#id_command_set-0-input').val('null');
    }

    function updateRecentCommands($, response) {
        if (isRecentCommandsAbsent()) {
            resetCommandForm();
            location.assign('#command_set-2-group');
            // If "Recent Commands" page is not available, hen wait for message
            // from websocket or 4 seconds whichever is earlier
            setTimeout(function () {
                location.reload();
            }, 4000);
            return;
        }

        let firstElement = $('#command_set-2-group fieldset .dynamic-command_set-2:first'),
            counter = (firstElement.attr('id')) ? String(Number(firstElement.attr('id').split('-')[2]) - 1) : '-1',
            element = $(getElement(response, counter));
        $('#id_command_set-2-MAX_NUM_FORMS').after(element);

        function getElement(response, counter) {
            let input,
                sentOn = gettext('sent on');
            if (response.input !== null) {
                if (response.input.command !== undefined) {
                    input = response.input.command;
                } else {
                    input = response.input;
                }
            } else {
                input = '';
            }
            return `<div class="inline-related has_original dynamic-command_set-2" id="command_set-2-${counter}">
                <h3><b>Recent Commands:</b>&nbsp;<span class="inline_label">«${response.type}» ${sentOn} ${dateTimeStampToDateTimeLocaleString(new Date(response.created))}</span></h3>
                    <fieldset class="module aligned ">
                    <div class="form-row field-status">
                        <div><label>Status:</label><div class="readonly">${response.status}</div></div>
                    </div>
                    <div class="form-row field-type">
                        <div><label>Type:</label><div class="readonly">${response.type}</div></div>
                    </div>
                    <div class="form-row field-input">
                        <div><label>Input:</label><div class="readonly">${input}</div></div>
                    </div>
                    <div class="form-row field-output">
                        <div><label>Output:</label><div class="readonly">${response.output}</div></div>
                    </div>
                    <div class="form-row field-created">
                        <div><label>Created:</label> <div class="readonly">${getFormattedDateTimeString(response.created)}</div></div>
                    </div>
                    <div class="form-row field-modified">
                        <div><label>Modified:</label><div class="readonly">${getFormattedDateTimeString(response.created)}</div></div>
                    </div>
                    </fieldset>
                <input type="hidden" name="command_set-2-${counter}-id" value="${response.id}" id="id_command_set-2-${counter}-id">
                <input type="hidden" name="command_set-2-${counter}-device" value="${response.device}" id="id_command_set-2-${counter}-device">
            </div>`;
        }
    }
}

function initCommandWebSockets($) {
    commandWebSocket.addEventListener('message', function (e) {
        let data = JSON.parse(e.data);
        // Done for keeping future use of these websocket
        if (data.model !== 'Command') {
            return;
        }
        // If "Recent Commands" is not present, then reload the page
        if (isRecentCommandsAbsent()) {
            location.reload();
        }

        data = data.data;
        let colorCode, input,
            commandIdInputField = $(`input[value="${data.id}"]`),
            commandObjectFieldset = commandIdInputField.parent().children('fieldset');

        if (data.input !== null) {
            if (data.input.command !== undefined) {
                input = data.input.command;
            } else {
                input = data.input;
            }
        } else {
            input = '';
        }

        commandObjectFieldset.find('.field-status .readonly').html(data.status);
        commandObjectFieldset.find('.field-input .readonly').html(input);
        commandObjectFieldset.find('.field-output .readonly').html(data.output);

        // Is it required to update modified timestamp?
        // We will require to to manipulation for rendering dates tp maintain consistency
        // with Django. I am not sure whether such solution won't break in different timezones(locales).
        commandObjectFieldset.find('.field-modified .readonly').html(getFormattedDateTimeString(data.modified));

        // Fade background color from green/red to white to signify change
        colorCode = (data.status == 'success') ? '#bbffbb' : '#ff949461';
        commandObjectFieldset.css('background-color', colorCode);
        setTimeout(function () {
            commandObjectFieldset.addClass('object-updated');
            commandObjectFieldset.css('background-color', 'inherit');
        }, 0);

    });

}

// Utility functions

function isRecentCommandsAbsent() {
    return document.getElementById('command_set-2-group') === null;
}

function getObjectIdFromUrl() {
    let objectId;
    try {
        objectId = /\/((\w{4,12}-?)){5}\//.exec(window.location)[0];
    } catch (error) {
        try {
            objectId = /\/(\d+)\//.exec(window.location)[0];
        } catch (error) {
            throw error;
        }
    }
    return objectId.replace(/\//g, '');
}

function getWebSocketProtocol() {
    let protocol = 'ws://';
    if (window.location.protocol === 'https:') {
        protocol = 'wss://';
    }
    return protocol;
}

function dateTimeStampToDateTimeLocaleString(dateTimeStamp) {
    let userLanguage = navigator.language || navigator.userLanguage,
        date = dateTimeStamp.toLocaleDateString(
            userLanguage, {
                day: 'numeric',
                month: 'short',
                year: 'numeric'
            }
        ),
        time = dateTimeStamp.toLocaleTimeString(
            userLanguage, {
                hour: 'numeric',
                minute: 'numeric',
                second: 'numeric'
            }
        ),
        at = gettext('at'),
        dateTimeString = `${date} ${at} ${time}`;
    return dateTimeString;
}

function getFormattedDateTimeString(DateTimeString) {
    let dateTime = new Date(DateTimeString),
        formattedString = dateTime.strftime('%B %d, %Y %I:%M %p'),
        stringArray = formattedString.split(' ');
    stringArray[0] = stringArray[0].substring(0, 4) + '.';
    stringArray[4] = (stringArray[4] == 'AM') ? 'a.m.' : 'p.m.';
    return stringArray.join(' ');
}
