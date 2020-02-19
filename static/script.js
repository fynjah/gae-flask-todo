;(function() {
    'use strict'
    window.Todo = function() {
        function Item(options) {
            return {
                'title': options['title'] || '',
                'checked': options['checked'] || false,
            }
        }

        this.build = function() {
            var _this = this,
                html = _this.renderItems(_this.listItems(), $('.todo-list'));
        }

        function Storage() {

            return {
                get: function() {
				    var $deferred = $.ajax({
				        type: "GET",
				        url: '/api/v1/todos',
				        dataType: 'json'
				    });
				    return $deferred;
                },
                create: function(item) {
				    var $deferred = $.ajax({
				        type: "POST",
				        url: '/api/v1/todos',
				        data:{
				        	"title":item.title
				        },
				        dataType: 'json'
				    });
				    return $deferred;
                },
                update: function(id, data) {
				    var $deferred = $.ajax({
				        type: "PUT",
				        url: '/api/v1/todos/'+id,
				        data:data,
				        dataType: 'json'
				    });
				    return $deferred;
                },
                delete: function(id) {
				    var $deferred = $.ajax({
				        type: "DELETE",
				        url: '/api/v1/todos/'+id,
				        dataType: 'json'
				    });
				    return $deferred;
                }
            }
        }

        this.storage = new Storage();

        this.addItem = function(title) {
            var _this = this,
            	title = title.trim(),
                item = new Item({
                    'title': title
                });
            if(!item.title){
                return;
            }
            return this.storage.create(item).success(function(data){
            	_this.build();
            });
            
        }

        function _renderItem(item) {
            var completed = (item.checked) ? 'completed' : '',
            	checked = item.checked ? 'checked' : '';
            return '<li class="todo-item" title="'+item.timestamp+'">\
            	<span class="checkbox">\
            	<input class="todo-checkbox" data-id="' + item.id + '" type="checkbox" '+checked+' /></span>\
            	<span class="title ' + completed + '">'+_.escape(item.title)+'</span>\
            	<span class="btn todo-delete" data-id="'+item.id+'"><button>×</button></span>\
            </li>';
        }
        this.renderItems = function(items, container) {
        	items.success(function(data){
	            var html = '';
	            _.each(data, function(item) {
	                html += _renderItem(item);
	            });
	            container.html(html);
        	})
        }
        this.checkItem = function(id, check) {
            return this.updateItem(id, {
                'checked': + check
            })
        }
        this.deleteItem = function(id) {
        	var _this = this;
            return this.storage.delete(id).success(function(data){
            	_this.build();
            });
        }
        this.updateItem = function(id, options) {
        	var _this = this;
            return this.storage.update(id, options).success(function(data){
            	_this.build();
            });
        }
        this.listItems = function() {
            return this.storage.get();
        }
    }
}).call(this);
