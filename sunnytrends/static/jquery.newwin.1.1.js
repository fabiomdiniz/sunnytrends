// jQuery newWin Plugin 1.0.1 (20100315)
// By John Terenzio | http://plugins.jquery.com/project/newwin | MIT License
(function($){$.fn.newWin=function(){return this.each(function(){if(this.protocol=='http:'&&this.hostname!=location.hostname){$(this).click(function(){open(this.href);return false;});}});};})(jQuery);