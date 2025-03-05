class t:
    new () :
        me.hello = "hello"
    ;
;
class ti < t:
    new ():
        me.hi = "hi"
        super.new()
    ;
    test (a) :
        a ++
    ;
;

fn add (n1 n2):
    return n1 + n2
;
fn test () :
    :
        var z = nil
    ;
    return z
;
fn main (args) :
    x = 5 + 3
    y = add(5 3)
    z = test()
;
