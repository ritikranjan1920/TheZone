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


var yes = 0;


function passWord(){
    document.getElementById('message').style.display = 'block';
    if(yes == 0){
        document.getElementById('s_password').classList.add("is-invalid");
    }else{
        document.getElementById('s_password').classList.add("is-valid");
    }
}

function validate(){
    var myInput = document.getElementById("s_password");
    var letter = document.getElementById("lower");
    var capital = document.getElementById("upper");
    var number = document.getElementById("number");
    var length = document.getElementById("character");
    var a = 1,b=1,c=1,d=1;

    if(myInput.value.match(/[a-z]/g)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
        a = 1;
    } else {
        a = 0;
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }

    // Validate capital letters

    if(myInput.value.match(/[A-Z]/g)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
        b = 1;
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
        b = 0;
    }

    // Validate numbers

    if(myInput.value.match(/[0-9]/g)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
        c = 1;
    } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
        c = 0;
    }

    // Validate length
    if(myInput.value.length >= 8) {
        length.classList.remove("invalid");
        length.classList.add("valid");
        d = 1;
    } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
        d = 0;
    }

    if(a==1 && b==1 && c==1 && d==1){
        myInput.classList.remove("is-invalid");
        myInput.classList.add("is-valid");
        yes = 1;
    }else{
        myInput.classList.remove("is-valid");
        myInput.classList.add("is-invalid");
        yes = 0;
    }

}

function click(){
    if(yes == 0){
    console.log("nO");
    }else{
    console.log("Yes");
    }
}

function change(){
    document.getElementById('s_password').classList.remove("is-valid");

    document.getElementById('message').style.display = 'none';
}

var yes1 = 0;

function passWord1(){
    document.getElementById('message1').style.display = 'block';
    if(yes1 == 0){
        document.getElementById('d_password').classList.add("is-invalid");
    }else{
        document.getElementById('d_password').classList.add("is-valid");
    }
}

function validate1(){
    var myInput = document.getElementById("d_password");
    var letter = document.getElementById("lower1");
    var capital = document.getElementById("upper1");
    var number = document.getElementById("number1");
    var length = document.getElementById("character1");
    var a = 1,b=1,c=1,d=1;

    if(myInput.value.match(/[a-z]/g)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
        a = 1;
    } else {
        a = 0;
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }

    // Validate capital letters

    if(myInput.value.match(/[A-Z]/g)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
        b = 1;
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
        b = 0;
    }

    // Validate numbers

    if(myInput.value.match(/[0-9]/g)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
        c = 1;
    } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
        c = 0;
    }

    // Validate length
    if(myInput.value.length >= 8) {
        length.classList.remove("invalid");
        length.classList.add("valid");
        d = 1;
    } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
        d = 0;
    }

    if(a==1 && b==1 && c==1 && d==1){
        myInput.classList.remove("is-invalid");
        myInput.classList.add("is-valid");
        yes1 = 1;
    }else{
        myInput.classList.remove("is-valid");
        myInput.classList.add("is-invalid");
        yes1 = 0;
    }

}

function change1(){
    document.getElementById('d_password').classList.remove("is-valid");


    document.getElementById('message1').style.display = 'none';
}

var yes2 = 0;

function passWord2(){
    document.getElementById('message2').style.display = 'block';
    if(yes2 == 0){
        document.getElementById('c_password').classList.add("is-invalid");
    }else{
        document.getElementById('c_password').classList.add("is-valid");
    }

}

function validate2(){
    var myInput = document.getElementById("c_password");
    var letter = document.getElementById("lower2");
    var capital = document.getElementById("upper2");
    var number = document.getElementById("number2");
    var length = document.getElementById("character2");
    var a = 1,b=1,c=1,d=1;

    if(myInput.value.match(/[a-z]/g)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
        a = 1;
    } else {
        a = 0;
        letter.classList.remove("valid");
        letter.classList.add("invalid");
    }

    // Validate capital letters

    if(myInput.value.match(/[A-Z]/g)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
        b = 1;
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
        b = 0;
    }

    // Validate numbers

    if(myInput.value.match(/[0-9]/g)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
        c = 1;
    } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
        c = 0;
    }

    // Validate length
    if(myInput.value.length >= 8) {
        length.classList.remove("invalid");
        length.classList.add("valid");
        d = 1;
    } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
        d = 0;
    }

    if(a==1 && b==1 && c==1 && d==1){
        yes2 = 1;
        myInput.classList.remove("is-invalid");
        myInput.classList.add("is-valid");
    }else{
        yes2 = 0;
        myInput.classList.remove("is-valid");
        myInput.classList.add("is-invalid");
    }

}

function change2(){
    document.getElementById('c_password').classList.remove("is-valid");

    document.getElementById('message2').style.display = 'none';
}


