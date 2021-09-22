function myFunction() {
    var input, filter, gdiv, div, a, adiv,h, txtValue, txtValue1, count=0;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    gdiv = document.getElementById("data");
    div = gdiv.getElementsByTagName("div");
    for (i = 0; i < div.length; i+=2) {
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

function filter() {
    var filter, data_div, div, label, value, count=0;
    filter = document.getElementById("filter");
    filter = filter.value.toUpperCase();
    data_div = document.getElementById("data");
    div = data_div.getElementsByTagName("div");
    for (i = 0; i < div.length; i+=2) {
        label = div[i].getElementsByTagName("h5")[0];
        value = label.innerText;
        if (value.toUpperCase().indexOf(filter) > -1) {
            div[i].style.display = "";
            document.getElementById("hidden").style.display = "none";
            count = count+1;
        }else if( filter == "FILTER" ){
            div[i].style.display = "";
            document.getElementById("hidden").style.display = "none";
            count = count+1;
        }else {
            div[i].style.display = "none";
        }
    }
    console.log(count);
    if(count == 0){
        document.getElementById("hidden").style.display = "block";
    }

}



function makeCSV() {
    var csv = "Name,RollNo.,Placement Info\n";
    var data_div, div, labels, value, count=0;
    data_div = document.getElementById("data");
    div = data_div.getElementsByTagName("div");
     for (i = 0; i < div.length; i+=2) {
        labels = div[i].getElementsByTagName("h5");
        if (div[i].style.display == "") {
            csv = csv + labels[1].innerText + "," + labels[2].innerText + "," + labels[0].innerText;
        }
        csv = csv+"\n";
    }
    console.log(csv);


    window.URL = window.URL || window.webkiURL;
    var blob = new Blob([csv]);
    var blobURL = window.URL.createObjectURL(blob);
    $("#csv").
    attr("href", blobURL).
    attr("download", "student_data.csv");
}