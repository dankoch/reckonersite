/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	
	config.FillEmptyBlocks = false;
	config.IgnoreEmptyParagraphValue = false;
	
	config.toolbar = 'Basic';
	config.toolbar_Basic =
		[
			['Bold', 'Italic', 'Underline', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink']
		];	
	 
	/* config.toolbar_Full =
	[
		{ name: 'document', items : [ 'Source','-','Save','NewPage','DocProps','Preview','Print','-','Templates' ] },
		{ name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
		{ name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ] },
		{ name: 'forms', items : [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 
	 
	         'HiddenField' ] },
		'/',
		{ name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
		{ name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-
	 
	        ','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
		{ name: 'links', items : [ 'Link','Unlink','Anchor' ] },
		{ name: 'insert', items : [ 'Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak','Iframe' ] },
		'/',
		{ name: 'styles', items : [ 'Styles','Format','Font','FontSize' ] },
		{ name: 'colors', items : [ 'TextColor','BGColor' ] },
		{ name: 'tools', items : [ 'Maximize', 'ShowBlocks','-','About' ] }
	]; */
};

CKEDITOR.on( 'dialogDefinition', function( ev )
		   {
		      // Take the dialog name and its definition from the event data.
		      var dialogName = ev.data.name;
		      var dialogDefinition = ev.data.definition;
		 
		      // Check if the definition is from the dialog we're
		      // interested in (the 'link' dialog).
		      if ( dialogName == 'link' )
		      {
		         // Remove the 'Target' and 'Advanced' tabs from the 'Link' dialog.
		         dialogDefinition.removeContents( 'target' );
		         dialogDefinition.removeContents( 'advanced' );
		 
		         // Get a reference to the 'Link Info' tab.
		         var infoTab = dialogDefinition.getContents( 'info' );
		 
		         // Remove unnecessary widgets from the 'Link Info' tab.         
		         infoTab.remove( 'linkType');
		         infoTab.remove( 'protocol');
		      }
		   }
);
