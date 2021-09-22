$(document).ready(function(){
          $('.tab a').on('click', function (e) {
          e.preventDefault();

          $(this).parent().addClass('active');
          $(this).parent().siblings().removeClass('active');

          var href = $(this).attr('href');
          $('.forms > form').hide();
          $(href).fadeIn(500);
        });
    });


$(function() {
    $('#account_picture').on('click', function() {
        $('#s_picture').trigger('click');
    });
});

$(function() {
    $('#placed_picture').on('click', function() {
        $('#picture').trigger('click');
    });
});

$(function() {
    $('#project_image').on('click', function() {
        $('#project_picture').trigger('click');
    });
});



function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#account_picture')
                .attr('src', e.target.result);
            $('#placed_picture')
                .attr('src', e.target.result);
            $('#placed_pic')
                .attr('src', e.target.result);
            $('#project_image')
                .attr('src', e.target.result);
            $('#project_edit_image')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function showSkills() {
    document.getElementById('less_skills').style.display = 'none';
    document.getElementById('more_skills').style.display = 'inline';
    document.getElementById('showLess').style.display = '';
    document.getElementById('showMore').style.display = 'none';
}

function hideSkills() {
    document.getElementById('less_skills').style.display = 'inline';
    document.getElementById('more_skills').style.display = 'none';
    document.getElementById('showLess').style.display = 'none';
    document.getElementById('showMore').style.display = '';
}






