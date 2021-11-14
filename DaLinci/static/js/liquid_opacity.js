$(document).ready(function() {
    $('#down-arrow').each(function(){
          $(this).animate({opacity:'0.3'},1);
          $(this).mouseover(function(){
              $(this).stop().animate({opacity:'1.0'},200);
          });
          $(this).mouseout(function(){
              $(this).stop().animate({opacity:'0.3'},100);
          });
    });
});