fn main(args) {
    var a := 3;
    println(a);
    var b := a:Num;
    println(b);
    var c := "5";
    println(add(b, c:Num));
}
fn add(a, b) {
    return a + b;
}
