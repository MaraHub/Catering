/**
 * Custom JS
 * Use this file to add your custom scripts
 */

  // $(document).ready(function(){
  //   $(".section_menu__item").click(function(){
  //     $(this).fadeOut( "slow",0.5,function(){} );
  //   });
  // });

  // $( ".section_menu__item" ).click(function() {
  //   $( this ).fadeTo( "slow", 0.33 );
  // });

  // $(".section_menu__item").toggle(
  // function() {
  //
  //     $(this).fadeTo( "slow", 0.33 );
  // },
  // function() {
  //
  //   $(this).fadeIn( "slow");
  // });

      // $(".section_menu__item").click(function () {
      //     $(this).toggle = !$(this).toggle;
      //     $(".section_menu__item").stop().fadeTo(400, this.toggle ? 0.4 : 1);
      // });

// General Use Functions
var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};
//var tech = getUrlParameter('technology');





      $( ".section_menu__item" ).click(function() {
        $(this).toggleClass('section_menu__item section_menu__item_selected')
      });

      // $( "h4" ).each(function( index ) {
      //   console.log( index + ": " + $( this ).text() );
      // });

      function put_to_array( divs ) {
        var a = [];
        for ( var i = 0; i < divs.length; i++ ) {
          console.log(divs[ i ].innerHTML );
          a.push(divs[ i ].innerHTML)
        } return a;
      }

  $(function() {
        $("#submit_menu_guest").click( function()
             {

               // alert('button clicked');
               var numselections = $('.section_menu__item_selected').length;
               var selections = $(".section_menu__item_selected .desserts").toArray();
                var entree = $(".section_menu__item_selected .entree").toArray();
                var kyriws = $(".section_menu__item_selected .kyriws").toArray();
                var desserts = $(".section_menu__item_selected .desserts").toArray();
                var drinks = $(".section_menu__item_selected .drinks").toArray();
               //var test = $('.section_menu__item_selected').serialize();
               //var cars = JSON.stringify(put_to_array(selections));
               console.log(put_to_array(selections).length);
               //console.log(typeof $(".section_menu__item_selected piato"));
               console.log(selections);
               $.ajax({

                  url: '/receiver',
                  type: 'POST',
                  dataType: 'json',
                  data:{ 'event_code':getUrlParameter('reservation__form__phone') ,
                          //'food':JSON.stringify(put_to_array(selections)),
                         'entree': JSON.stringify(put_to_array(entree)),
                         'kyriws': JSON.stringify(put_to_array(kyriws)),
                         'desserts': JSON.stringify(put_to_array(desserts)),
                         'drinks': JSON.stringify(put_to_array(drinks)),
                        'voter':getUrlParameter('reservation__form__name')
                      },
                  success:function(json)
                                {
                                    alert(json.result);  //response from the server given as alert message
                                }
                      });

               if (numselections>1){
                 console.log('Please select less than 2');
               }

             }
        );
  });
