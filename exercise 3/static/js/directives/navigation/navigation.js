app.directive("navigation", ['$compile', function ($compile) {
	return {
		scope: {
			menu: '='
		},
		restrict: 'E',
		replace: true,
		templateUrl: 'js/directives/navigation.html',
		compile: function (elem) {
			var contents = elem.contents().remove();
			return function(scope, el){
				if(typeof compiled == 'undefined') {
					compiled = $compile(contents);
				}
				
				if(typeof compiled !== 'undefined') {
					compiled(scope,function(clone){
						el.append(clone);
					})
				};
			}
		}
	}
}]);