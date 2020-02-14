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
				        url: '/json',
				        dataType: 'json'
				    });
				    return $deferred;
                },
                create: function(title) {
				    var $deferred = $.ajax({
				        type: "POST",
				        url: '/json',
				        data:{
				        	title:title
				        },
				        dataType: 'json'
				    });
				    return $deferred;
                },
                update: function(item) {
				    var $deferred = $.ajax({
				        type: "PUT",
				        url: '/json',
				        dataType: 'json'
				    });
				    return $deferred;
                },
                delete: function(id) {
				    var $deferred = $.ajax({
				        type: "DELETE",
				        url: '/json',
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
            this.storage.create(item).success(function(data){
            	_this.build();
            });
            
        }

        function _renderItem(item) {
            var completed = (item.checked) ? 'complete' : "";
            return '<li class="todo-item ' + completed + '" title="'+item.timestamp+'">\
            	<span class="checkbox"><input data-id="' + item.id + '" type="checkbox" /></span>\
            	<span class="title">'+_.escape(item.title)+'</span>\
            	<span class="btn"><button class="close" data-dismiss="alert">×</button></span>\
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
        this.getItem = function(id) {

        }
        this.checkItem = function(id, check) {
            this.updateItem(id, {
                'checked': Boolean(check)
            })
        }
        this.deleteItem = function(id) {

        }
        this.updateItem = function(id, options) {

        }
        this.listItems = function() {
            return this.storage.get();
        }
    }
}).call(this);
