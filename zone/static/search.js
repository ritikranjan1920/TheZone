function myFunction() {
    var input, filter, gdiv, div, a, adiv,h, txtValue, txtValue1, count=0;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    gdiv = document.getElementById("data");
    div = gdiv.getElementsByTagName("div");
    for (i = 0; i < div.length-1; i++) {
        a = div[i].getElementsByTagName("a")[0];
        adiv = a.getElementsByTagName("div")[0];
        h = adiv.getElementsByTagName("h5");
        txtValue = h[0].textContent || h[0].innerText;
        txtValue1 = h[1].textContent || h[1].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1 || txtValue1.toUpperCase().indexOf(filter) > -1) {
            div[i].style.display = "";
            document.getElementById("hidden").style.display = "none";
            count = count+1;
        } else {
            div[i].style.display = "none";
        }
    }
    console.log(count);
    if(count == 0){
    document.getElementById("hidden").style.display = "block";
    }
}