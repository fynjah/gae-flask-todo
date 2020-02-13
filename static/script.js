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


            $('.todo-list').html(html);
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
                create: function(items) {
				    var $deferred = $.ajax({
				        type: "POST",
				        url: '/json',
				        dataType: 'json'
				    });
				    return $deferred;
                },
                update: function(items) {
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

        this.addItem = function(title, status) {
            var _this = this,
            	title = title.trim(),
                item = new Item({
                    'title': title,
                    'status': status
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
            console.log(item)
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
        this.getItemIndex = function(id) {
            var items = this.listItems();
            return _.findIndex(items, {
                'id': id
            });
        }
        this.getItem = function(id) {
            var items = this.listItems();
            return items[this.getItemIndex(id)];
        }
        this.checkItem = function(id, check) {
            this.updateItem(id, {
                'checked': Boolean(check)
            })
        }
        this.deleteItem = function(id) {
            var items = this.listItems(),
                index = this.getItemIndex(id);

            if (index > -1) {
                items.splice(index, 1)
            }
            this.storage.update(items);
        }
        this.updateItem = function(id, options) {
            options || (options = {});
            var items = this.listItems(),
                index = this.getItemIndex(id);
            _.assign(items[index], options)
            this.storage.update(items);
        }
        this.listItems = function() {
            return this.storage.get();
        }
    }
}).call(this);
