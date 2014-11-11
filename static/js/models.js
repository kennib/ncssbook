var WallPostModel = Class.create(Model, {
  initialize: function($super, person_id) {
    $super();
    this.plural_path = "/person/" + person_id + "/posts/";
    this.person_id = person_id;
  },
  
  path: function() {
    return "/person/" + this.person_id + "/post/" + this.get('id') + "/";
  },
  
  create: function() {
    return new WallPost(this.person_id);
  }
});


var PersonModel = Class.create(Model, {
  initialize: function($super) {
    $super();
    this.plural_path = "http://localhost:8888/cgi-bin/facebook/ncssbook/people/";
  },
  
  path: function() {
    return "http://localhost:8888/cgi-bin/facebook/ncssbook/person/" + this.get('id') + "/";
  },
  
  create: function() {
    model = new PersonModel();
    model.addObserver('id', model);
    return model;
  },
  
  keyWillUpdate: function(person, key, currentValue, newValue) {
    if(!currentValue && newValue)
      this.wallPostModel = new WallPostModel(newValue);
  },
  
  keyDidUpdate: function(person, key, value) {}
});

var Person = new PersonModel();
