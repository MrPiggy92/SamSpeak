#bob
fn factorial_iterative (n) {
    if (n < 0) return 1;
    var result := 1;
    for (var i := 1; i <= n; i ++) {
        result *= i;
    }
    return result;
}
fn factorial_recursive (n) {
    if (n < 0) return 1;
    else if (n == 0 or n == 1) return 1;
    else return n * factorial_recursive (n-1);
}

fn factorial () {
    var num := input("Enter a number: ");
    num = num :Num;
    num = round(num);
    var result_iterative := factorial_iterative (num);
    var result_recursive := factorial_recursive (num);
    result_iterative = result_iterative :Str;
    result_recursive = result_recursive :Str;
    println("Factorial iterative: " + result_iterative);
    println("Factorial recursive: " + result_recursive);
}
