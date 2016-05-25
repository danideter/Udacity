app.directive("comment", function () {
	return {
		controller: "CommentController",
		controllerAs: "cmmtCtrl",
		scope: {
			movieshow: '=',
			scienceshow: '=',
			comment: '=',
			schema: '=',
			currentuser: '=',
			science: '='
		},
		restrict: 'E',
		replace: true,
		templateUrl: 'js/directives/comment/comment.html',
	}
});