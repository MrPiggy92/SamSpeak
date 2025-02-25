!io
//#hi
class test :
    new () :
        println("hello")
        println(me)
        me.h = "what"
    ;
    sayWhat () :
        println(me.h)
    ;
    hi () :
        println("hi")
    ;
;
fn main (args) :
    test.hi()
    var h = test.new()
    println(h)
    h.sayWhat()
;
