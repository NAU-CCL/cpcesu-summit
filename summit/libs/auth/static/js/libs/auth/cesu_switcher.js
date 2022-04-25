$(".pop").popover({ trigger: "manual" , html: true, animation:false})
    .on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(".popover").on("mouseleave", function () {
            $(_this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide");
            }
        }, 300);
});

var change_cesu = function(cesu_id){
  $.ajax({
      type: "GET",
      url: '/projects/change_cesu',
      data: {'cesu_id': cesu_id},
      success: function(resp){
          window.location.href = "/projects/dashboard/";
          console.log(resp)
      }})
}