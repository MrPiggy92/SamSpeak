!persist
!io
!data

fn load_file (file) :
    file += ".yml"
    var data = loadf("yaml" file)
    return data
;

fn ask_question (question) :
    var text = question["Q"]
    text += " ("
    for (var i = 0; i < length(question["A"]); i ++) :
        text += question["A"][i]
        text += "/"
    ;
    text += "IDC"
    text += ")"
    println(text)
    var ans = input(" > ")
    while ( !(ans in question["A"]) and ans != "IDC") :
        println("That is not an option.")
        ans = input (" > ")
    ;
    return ans
;

fn ask_questions (questions) :
    var answers = []
    var ans
    for (var i = 0; i < length(questions); i ++) :
        ans = ask_question(questions[i])
        answers += ans
    ;
    return answers
;

fn result_ok (answers result) :
    var num
    for (var i = 0; i < length (answers); i ++) :
        num = "Q" + (i+1 :Str)
        //println(answers[i])
        //println(result[num])
        if (answers[i] != result[num] and answers[i] != "IDC"):
            //println("fail")
            return false
        ;
    ;
    return true
;

fn filter_results (answers results) :
    var passes = []
    for (var i = 0; i < length(results); i ++) :
        if (result_ok(answers results[i])):
            passes += results[i]
        ;
    ;
    return passes
;

fn output_passes (passes) :
    if (length(passes) > 3) :
        println("There are many deserts we have for you!")
        for (var i = 0; i < length(passes); i ++) :
            println(passes[i]["name"])
        ;
    ; else :
        var text = "The perfect desert for you is "
        for (var i = 0; i < length(passes); i ++) :
            text += passes[i]["name"]
            if (i != length(passes) - 1 ) :
                text += " or "
            ;
        ;
        text += "!"
        println(text)
    ;
;

fn main (args) :
    var data = load_file ("desertsQuiz")
    //println(data)
    var answers = ask_questions(data["questions"])
    //println(answers)
    var passes = filter_results(answers data["results"])
    //println(passes)
    output_passes(passes)
;
