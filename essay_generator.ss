fn build_graph(text) {
    var words = split(text);
    var G = {};
    for (var i = 0; i < length(words)-1; i ++) {
        //println(i);
        if (words[i] in keys(G)) {
            //println("in");
            G[words[i]] += words[i+1];
        } else {
            //println("not in yet");
            G[words[i]] = [words[i+1]];
        }
    }
    return G;
}
fn generate_graph(graph, output_length) {
    var words = keys(graph);
    var wordIndex = random();
    wordIndex *= length(words);
    wordIndex = round(wordIndex);
    var word = words[wordIndex];
    //println(word);
    var generated = [];
    for (var i = 0; i < output_length - 1; i ++) {
        if (word in graph) {
            wordIndex = random();
            wordIndex *= length(graph[word])-1;
            wordIndex = round(wordIndex);
            //println(graph[word][wordIndex]);
            word = graph[word][wordIndex];
        } else {
            wordIndex = random();
            wordIndex *= length(words)-1;
            wordIndex = round(wordIndex);
            word = words[wordIndex];
        }
        generated += word;
    }
    return generated;
}
fn main (args) {
    var sample_text = "The life of a Roman legionary was one of discipline, duty, and hardship. A typical day began before dawn with the sound of a trumpet, signaling the soldiers to wake. They quickly donned their tunics and armor, fastening their belts and securing their gladii at their sides. Breakfast was simple—usually a portion of bread, porridge, and watered-down wine.

After eating, the soldiers assembled for inspection. Their centurion, a hardened veteran, ensured that every piece of equipment was in top condition. A Roman soldier’s kit was extensive, including a helmet, chain mail or segmented armor, a large rectangular shield, and javelins. Any soldier found with a poorly maintained weapon risked harsh punishment.

The morning was often spent drilling. Training was relentless, even in peacetime. Soldiers practiced marching in formation, thrusting their swords with precision, and hurling javelins at targets. They performed these exercises in full armor to build endurance. Discipline was paramount—every man had to know his place in the line, react swiftly to orders, and move as a single unit.

By midday, the men would break for a meal, often consisting of more bread, cheese, olives, and dried meat. If the legion was stationed at a fort, some soldiers would rotate through guard duty or work on construction projects. Roman forts were constantly expanded or reinforced, and soldiers were expected to dig ditches, repair walls, or build roads when not on campaign.

The afternoon might involve more drills, weapon maintenance, or lessons in tactics and Roman military law. Officers occasionally held mock battles, ensuring that the legionaries were always prepared for real combat. Those not assigned to these tasks might spend time in the bathhouse, discussing the latest news from Rome or gambling with dice.

As evening approached, another meal was served, and men would gather around fires to talk, play board games, or write letters home. Life in the legion was tough, but it offered a steady wage, the promise of land upon retirement, and the camaraderie of fellow soldiers.

Before nightfall, the watch was set. Those assigned to guard duty patrolled the walls of the camp, ever vigilant for enemy movements. The rest of the legionaries settled into their tents, knowing that tomorrow would bring another day of discipline, duty, and the ever-present possibility of battle.";
    var graph = build_graph(sample_text);
    //println(graph);
    var output = generate_graph(graph, 50);
    println(output);
}
    
