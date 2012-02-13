/*
 * jQuery File Upload Plugin JS Example 5.1.5
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://creativecommons.org/licenses/MIT/
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload();

    $('#fileupload').fileupload('option', {
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
    	autoUpload: true,
        maxFileSize: 256000,
        maxNumberOfFiles: 2,
        url: "ajax/reckoning/image/upload"
    });
    
    // Add the uploaded file path to the correct field of the form.
    $('#fileupload').bind('fileuploaddone', function (e, data) {
        var that = $(this).data('fileupload');
        if (data.context) {
            data.context.each(function (index) {
                var file = ($.isArray(data.result) &&
                        data.result[index]) || {error: 'emptyResult'};
                if (!file.error) {
                	var origValue = $("#attached-files").attr("value");
                	$("#attached-files").attr("value", file.url + ";" + origValue)
                }
            });
        } 
    });
    
    // Remove the deleted file path from the correct field of the form.
    $('#fileupload').bind('fileuploaddestroy', function (e, data) {
        var that = $(this).data('fileupload');
        if (data.context) {
        	// Get the submitted ID by taking the submission URL, removing trailing spaces, splitting by '/', and taking the last value.
        	var submitSegments = data.url.split(" ").join("").split("/");
        	var id = submitSegments[submitSegments.length - 1];
        	
        	var origValue = $("#attached-files").attr("value");
        	var newValue = "";
        	
        	var origFiles = origValue.split(';')
        	for (var i = 0; i < origFiles.length; i ++) {
        		if (origFiles[i] != "" && origFiles[i].indexOf(id) == -1) {
        			newValue += origFiles[i] + ";";
        		}
        	}
        	
        	$("#attached-files").attr("value", newValue);
        } 
    });

    // Enable iframe cross-domain access via redirect page:
    var redirectPage = window.location.href.replace(
        /\/[^\/]*$/,
        '/result.html?%s'
    );
    $('#fileupload').bind('fileuploadsend', function (e, data) {
        if (data.dataType.substr(0, 6) === 'iframe') {
            var target = $('<a/>').prop('href', data.url)[0];
            if (window.location.host !== target.host) {
                data.formData.push({
                    name: 'redirect',
                    value: redirectPage
                });
            }
        }
    });

    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files').delegate(
        'a:not([rel^=gallery])',
        'click',
        function (e) {
            e.preventDefault();
            $('<iframe style="display:none;"></iframe>')
                .prop('src', this.href)
                .appendTo(document.body);
        }
    );

    // Initialize the Image Gallery widget:
    $('#fileupload .files').imagegallery();
});
