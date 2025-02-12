!data
!io

fn main(args) :
    var arr = [3 9 5 7 8 6 4]
    var n = length(arr)
    for (var i = 0; i < n-1; i ++) :
        for (var j = 0; j < n-i-1; j ++) :
            if (arr[j] > arr[j+1]) :
                var temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
            ;
        ;
    ;
    println(arr)
;
