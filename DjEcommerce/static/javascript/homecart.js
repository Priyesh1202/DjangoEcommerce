function myfunction()
{
    var x = document.getElementsByClassName("money");
    var q = document.getElementsByClassName("q");
    var round = Math.round;
    var total = round(0);
    for (var i = 0; i < x.length; i++){
        var price = round(x[i].innerText);
        var quan = round(q[i].innerText);
        var t = round(price*quan)
        total = total+t;
    }
    document.getElementById(2).innerText = total;
}