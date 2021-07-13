$('#search-show-more-button').on('click', function(){
  $(document.getElementById('search-show-more')).removeClass("invisible");
  $(document.getElementById('search-show-more-button')).addClass("invisible");
  $(document.getElementById('search-show-less-button')).removeClass("invisible");
})

$('#search-show-less-button').on('click', function(){
  $(document.getElementById('search-show-more')).addClass("invisible");
  $(document.getElementById('search-show-less-button')).addClass("invisible");
  $(document.getElementById('search-show-more-button')).removeClass("invisible");
})


