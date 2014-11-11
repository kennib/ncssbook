Event.observe(window, 'load', function(){
	// wall posts
	Event.observe('comment_form', 'submit', function(event) {
	    $('comment_form').request({
	        onFailure: function() {},
	        onSuccess: function(t) {
	            $('wall_posts').update(t.responseText);
	        }
	    });
	    Event.stop(event); // stop the form from submitting
	});

	// How to update the wall
	new Ajax.Updater('wall_posts', '/wall', {
	  parameters: { profile_id: $('profile_id').value},
	  method: "GET"
	});
	
	// Clear the default comment box contents
	Event.observe('comment_box', 'click', function(event){
		$('comment_box').value = '';
	});
	

	/* Search related js
	 */
//	Event.observe('search_form', 'submit', function(event) {
//	    $('search_form').request({
//	        onFailure: function() {},
//	        onSuccess: function(t) {
//	            $('friend_results').update(t.responseText);
//	        }
//	    });
//	    Event.stop(event); // stop the form from submitting
//	});
//	
//	// How to update the search results
//	new Ajax.Updater('friend_results', 'cgi_scripts/friend_search.cgi', {
//		parameters: { query: $('query').value},
//		method: "GET"
//	});
//
//	// Clear the default search box contents
//	Event.observe('search_box', 'click', function(event){
//		$('search_box').value = '';
//	});
	

	/* Friend related js
	 */
	Event.observe('friend_button', 'click', function(event){
		new Ajax.Updater('friend_list', '/add', {
			parameters: { user_id: $('from_id').value,
				profile_id: $('to_id').value}
		});
	});

	// How to update the friend list
	new Ajax.Updater('friend_list', '/profile', {
		parameters: { profile_id: $('to_id').value },
		method: "GET"
	});
});
