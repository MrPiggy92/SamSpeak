fn main (args) {
    println("hi");
    run(lm () {println("hello");});
    fn hi () {println("helo");}
    run(hi);
    lm (n) {println("bye");println(n);} (5);
}
fn run (fun) {
    fun();
}
//TODO maps preprocessor bootstrap
