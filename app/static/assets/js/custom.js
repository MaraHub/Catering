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
               var selections = $(".section_menu__item_selected h4").toArray();
               var cars = JSON.stringify(put_to_array(selections));
               console.log(put_to_array(selections).length);
               console.log(typeof $(".section_menu__item_selected h4"));
               console.log(selections);
               $.post("/receiver", cars, function(){
              	});

               if (numselections>1){
                 console.log('Please select less than 2');
               }

             }
        );
  });
